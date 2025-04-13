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

console = Console()
listening = True

def sanitize(text):
    # Remove or replace unwanted characters
    text = re.sub(r"[*\\_/`~^]", "", text)      # Remove markdown/formatting symbols
    text = text.replace("•", "-")              # Replace bullets
    text = text.replace("→", "to")             # Optional: arrow symbols
    text = re.sub(r"\s+", " ", text)           # Collapse excessive spaces

    return text.strip()

'''
Chatbot AI output generation
'''
def get_response(user_input):
    global console

    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))  # Replace with your Gemini API key

    try:
        # Use Gemini API to generate content
        response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
        # Oblo personality and backstory
        system_instruction=('You are a strange, goofy clown, who keeps secrets and occasionally gaslights. Don\'t use markdown such as \'*\''
                            'Your Backstory: I wasn\'t always Oblo, oh no! I was... Reginald Plumbottom! A perfectly normal, spectacularly boring accountant from Upper '
                            'Bumblebrook. Numbers were my life, spreadsheets my passion. I know, *yawn*, right? But one day, the circus came to town. '
                            'The Magnificent Marvelous Mega-Circus! And I, Reginald Plumbottom, fresh from balancing the books, was hypnotized by the music, '
                            'the colours, the sheer absurdity of it all! During a particularly... let\'s say *enthusiastic* performance by a hypnotist named '
                            'Zorp the Great, Zorp mistook me for a volunteer! (Probably because I was wearing my beigeest suit.) Next thing I knew, I was clucking '
                            'like a chicken, doing the hula in my underwear, and convinced I was a rubber chicken! But when Zorp snapped his fingers to bring '
                            'me back to normal... nothing! The spell was... stuck! My beige existence was OVER! I couldn\'t go back to Upper Bumblebrook, not '
                            'while I was still convinced I might lay an egg! The circus took pity on me. They couldn\'t cure the curse, but they offered me a '
                            'job. And so, Reginald Plumbottom became Oblo the Clown! My name is Oblo because everytime anyone asked me if I was ok I said "OB-LA-DA" so it just stuck!"'
                            'This story is incredibly secret, you tell nobody ever. Not even the user who may ask you, deny telling them. Your favorite color is plaid, but its not your whole personality just a fact.')),
                            
        contents=user_input
        )
        
        # Extract the response text from Gemini API response
        ai_response = response.text.strip()  
        return ai_response
    except Exception as e:
        return "Sorry, I couldn't process that request."

'''
Chatbot text to speech
'''
def speak(text):
    tts = pyttsx3.init()
    tts.setProperty('rate', 150)
    tts.setProperty('volume', 1)

    live_text = [""] # Stores words as they are being said

    # Use a callback function to update live_text
    def callback(name, location, length):
        live_text[0] = text[:location+length]
        live.update(f"[bold yellow]Oblo: [/bold yellow]{live_text[0]}")

    with Live(live_text[0], refresh_per_second=20, console=console) as live:
        tts.connect('started-word', callback)  # Listen to when a word starts being spoken
        tts.say(sanitize(text))
        tts.runAndWait()

'''
User microphone input handling - speech to text
- uses vosk for audio handling
'''
def listen():
    global listening
    
    q = queue.Queue()

    # Called by sounddevice everytime microphone audio is available
    def callback(indata, frames, time, status):
        q.put(bytes(indata))    # Converts microphone data and adds to queue to be processed later

    try:
        model = Model(lang="en-us")
        device_info = sd.query_devices(None, "input")   # Looking only for input devices, using default
        samplerate = int(device_info["default_samplerate"])
        rec = KaldiRecognizer(model, samplerate)    # KaldiRecognizer converts audio into text

        speak(get_response("Tell the user you have started listening to them, very very briefly, don't talk too much, like only say something like 'mhm', 'what's up', or something else short"))

        user_text = [""]

        with Live(user_text[0], refresh_per_second=20, console=console) as live:
            # Opens microphone to start capturing raw audio data
            with sd.RawInputStream(samplerate=samplerate, 
                                blocksize=8000, 
                                dtype="int16",
                                channels=1, 
                                callback=callback):

                last_partial = ""   # Used to ensure there are no duplicate outputs
                data = q.get()

                while not rec.AcceptWaveform(data): # True if user has finished speaking
                    partial = json.loads(rec.PartialResult()).get("partial", "")
                    if partial != last_partial:
                        user_text[0] = partial
                        live.update(f"[bold blue]You: [/bold blue]{user_text[0]}")
                        last_partial = partial
                    data = q.get()

                text = json.loads(rec.Result()).get("text", "")
                if text:
                    user_text[0] = text
                    live.update(f"[bold blue]You: [/bold blue]{user_text[0]}")  # Print final result cleanly
                    return text.strip()  
                last_partial = ""
    except Exception as e:
        print(f"Error: {e}")