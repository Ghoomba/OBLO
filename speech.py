import os
import queue
import sounddevice as sd                   # Speech Recognition 
from vosk import Model, KaldiRecognizer 
import json
import pyttsx3                             # Text to speech
from google import genai                   # AI Generated responses
from google.genai import types         
from rich.console import Console           # Text Formatting
from rich.live import Live
import re
from dotenv import load_dotenv
import keyboard
import time
import yaml
# from display import animate              # Handle Animation here for clear screens

user_text = ""

# Load the config file
with open("settings.yml") as file:
    config = yaml.safe_load(file)

load_dotenv()   # Use a .env for API keys

console = Console()
listening = True

ai_config = config['ai']
history = []    # Dictionary of current sessions chat history | {role: oblo/user, content: msg}

# MESSAGE HISTORY HANDLING
class History:
    # MESSAGE HISTORY STR CONVERSION #
    def to_string(history: dict):
        converted_history = ''

        for msg in history:
            match msg['role']:
                case 'instruction':
                    converted_history += f'Instruction: {msg['content']}\n'
                case 'user':
                    converted_history += f"User: {msg['content']}\n"
                case 'oblo':
                    converted_history += f"Oblo: {msg['content']}\n"

        converted_history += "Oblo: "

        return converted_history  # Return the history dictionary as a string

    # ADD TO HISTORY
    def add(role: str, text: str):
        match role:
            case 'user':
                history.append({'role': 'user', 'content': f"{text}\n"})
            case 'oblo':
                history.append({'role': 'oblo', 'content': f"{text}\n"}) 
            case 'instruction':
                history.append({'role': 'oblo', 'content': f"{text}\n"})

        return text
            
            
# AI OUTPUT GENERATION
def get_response():
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))  # Replace with your Gemini API key

    try:
        # Use Gemini API to generate content
        response = client.models.generate_content(
            model=ai_config['model'],
            config=types.GenerateContentConfig(
                system_instruction=(ai_config['instruction'])), # Oblo personality and backstory
            contents=History.to_string(history)
        )
        
        # Extract the response text from Gemini API response
        ai_response = response.text.strip()

        return ai_response
    except Exception as e:
        return "Sorry, I couldn't process that request."


# TEXT TO SPEECH #
def speak(text):
    global config
    tts_config = config['tts']

    tts = pyttsx3.init()
    tts.setProperty('rate', tts_config['rate'])
    tts.setProperty('volume', tts_config['volume'])

    live_text = [""] # Stores words as they are being said

    # Use a callback function to update live_text
    def callback(name, location, length):
        live_text[0] = text[:location+length]
        live.update(f"[bold yellow]Oblo: [/bold yellow]{live_text[0]}\n")

    with Live(live_text[0], refresh_per_second=20, console=console) as live:
        tts.connect('started-word', callback)  # Listen to when a word starts being spoken
        tts.say(text)
        tts.runAndWait()

'''
User microphone input handling - speech to text
- uses vosk for audio handling
'''
def listen():
    global config
    global user_text
    q = queue.Queue()

    speech_config = config['speech-recognition']

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    try:
        model = Model(lang="en-us")
        device_info = sd.query_devices(None, "input")
        samplerate = int(device_info["default_samplerate"])
        rec = KaldiRecognizer(model, samplerate)

        history.append({'role': 'instruction', 'content': 'Say something short like \'listening\' or \'okay\' to let the user know you\'re listening\n'})
        
        speak(history.append({'role': 'oblo', 'content': f"{get_response()}\n"}))

        user_text = [""]
        final_result = []
        last_partial = ""

        with Live(user_text[0], refresh_per_second=speech_config['refresh'], console=console) as live:
            with sd.RawInputStream(samplerate=samplerate,
                                   blocksize=speech_config['blocksize'],
                                   dtype=speech_config['dtype'],
                                   channels=speech_config['channels'],
                                   callback=callback):

                # Wait for spacebar to be released (in case it’s still held down)
                while keyboard.is_pressed('space'):
                    time.sleep(0.1)

                while not keyboard.is_pressed("space"):
                    if not q.empty():
                        data = q.get()
                        if rec.AcceptWaveform(data):
                            result = json.loads(rec.Result()).get("text", "")
                            if result:
                                final_result.append(result)
                        else:
                            partial = json.loads(rec.PartialResult()).get("partial", "")
                            if partial != last_partial:
                                user_text[0] = partial
                                live.update(f"[bold blue]You: [/bold blue]{user_text[0]}")
                                last_partial = partial
                    else:
                        time.sleep(0.01)

        # Clean up final result
        final_text = " ".join(final_result).strip()
        if final_text:
            user_text[0] = final_text
            return final_text
        return ""

    except Exception as e:
        print(f"Error: {e}")
        return ""
    



























    
def sanitize(text):
    # Remove or replace unwanted characters
    text = re.sub(r"[*\\_/`~^]", "", text)      # Remove markdown/formatting symbols
    text = text.replace("•", "-")              # Replace bullets
    text = text.replace("→", "to")             # Optional: arrow symbols
    text = re.sub(r"\s+", " ", text)           # Collapse excessive spaces

    return text.strip()
