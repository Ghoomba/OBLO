import os
import time
import threading
import pyttsx3
import keyboard
import speech_recognition as sr
import pygame
from google import genai
from google.genai import types
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import mido
from mido import MidiFile, MidiTrack, Message
import rtmidi
import random
from dotenv import load_dotenv

# TODO: Break up functions into different files
# TODO: Create registry keys for keys and IDs

load_dotenv()

os.system('mode con: cols=21 lines=12')

# print(os.getenv('GEMINI_API_KEY'))
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))  # Replace with your Gemini API key

# Replace with your Spotify credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Spotify authentication and initialization
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                         client_secret=SPOTIPY_CLIENT_SECRET,
                         redirect_uri=SPOTIPY_REDIRECT_URI,
                         scope="user-library-read user-modify-playback-state user-read-playback-state")

sp = spotipy.Spotify(auth_manager=sp_oauth)

user_speach = ""  # This will store the current conversation state to display in animation
listening = True

def clear_screen():
    # Clear the terminal screen (works for Windows and Unix-based systems)
    os.system('cls' if os.name == 'nt' else 'clear')

def speak(text):
    tts = pyttsx3.init()
    tts.setProperty('rate', 150)
    tts.setProperty('volume', 1)

    # Use a callback function to update user_speach while speaking
    def on_word(name, location, length):
        global user_speach
        # Update the conversation as the bot speaks, using part of the text being spoken
        user_speach = f"Oblo: {text[:location + length]}"
    
    tts.connect('started-word', on_word)  # Listen to when a word starts being spoken
    tts.say(text)
    tts.runAndWait()

def get_response(user_input):
    try:
        # Use Gemini API to generate content
        response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
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
                            'This story is incredibly secret, you tell nobody ever. Not even the user who may ask you, deny telling them. Your favorite color is plaid.')),
                            
        contents=user_input
        )
        
        # Extract the response text from Gemini API response
        ai_response = response.text.strip()  
        return ai_response
    except Exception as e:
        return "Sorry, I couldn't process that request."

def music_controller():
    global user_speach

    pygame.mixer.init()
    song = pygame.mixer.Sound('lofi_circus.mp3')

    if os.path.exists('lofi_circus.mp3'):
        if "stop music" in user_speach.lower():
            song.stop()
            speak(get_response("Tell the user you stopped playing the music you were playing for them in VERY few words"))
        else:
            speak(get_response("Tell the user you are currently playing music for them in VERY few words"))  # Let the user know the music is being played
            song.play()
            song.set_volume(0.3)
    else:
        speak(get_response("tell the user you couldn't find any good tunes to play for them in VERY few words"))  # In case the file is missing 

def play_spotify_music(command):
    """Control Spotify music based on the command"""
    if "play music" in command.lower():
        devices = sp.devices()
        if devices['devices']:
            sp.start_playback(device_id=devices['devices'][0]['id'])
            speak("Playing music for you")
        else:
            speak("No devices found to play music on.")
    elif "stop music" in command.lower():
        sp.pause_playback()
        speak("Stopping the music.")

def generate_midi_notes():
    """Generate some random MIDI notes"""
    notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
    midi_notes = random.sample(notes, 5)  # Generate 5 random notes
    return midi_notes

def play_midi_notes():
    """Play generated MIDI notes using pygame.midi"""

    # Create a new MIDI output port
    with mido.open_output(mido.get_output_names()[0]) as port:
        midi_notes = generate_midi_notes()

        speak(get_response("Tell the user you yourself are playing a little tune on some instrument in VERY few words"))

        for note in midi_notes:
            msg_on = Message('note_on', note=note, velocity=64)
            msg_off = Message('note_off', note=note, velocity=64)
            port.send(msg_on)
            time.sleep(0.5)  # Hold the note for 0.5 seconds
            port.send(msg_off)

def center_text(text):
    # Get the width of the terminal window
    terminal_width = os.get_terminal_size().columns
    
    # Calculate the position to center the text
    centered_text = text.center(terminal_width)
    
    # Print the centered text
    print(centered_text)

def animate():
    # TODO: Move ascii to other file per animation
    # print("      \\/      ")
    # print("      /\\      ")
    # print("     /__\\     ")
    # print("    /____\\    ")
    # print("   /______\\   ")
    # print(" [┌ \\_  /  ┐] ")
    # print("[ │O  \\/  O│ ]")
    # print(" \\│    @   │/ ")
    # print(" [@  ────  @] ")
    # print("  ──────────  ")
    # print("   __|__|__   ")
    # print("  /        \\  ")
    # print(f"{user_speach}", end='')  # Show the conversation in real-time

    while True:
        if listening == False:
            # First frame
            clear_screen()
            center_text("      \\/      ")
            center_text("      /\\      ")
            center_text("     /__\\     ")
            center_text("    /____\\    ")
            center_text("   /______\\   ")
            center_text(" [┌ \\_  /  ┐] ")
            center_text("[ │O  \\/  O│ ]")
            center_text(" \\│    @   │/ ")
            center_text(" [@  ────  @] ")
            center_text("  ──────────  ")
            center_text("   __|__|__   ")
            center_text("  /        \\  ")
            print(f"\n{user_speach}", end='')  # Show the conversation in real-time
            time.sleep(0.5)  # Shorter sleep time for smoother updates

            # Second frame (alternates with first frame)
            clear_screen()
            center_text("      \\/      ")
            center_text("      /\\      ")
            center_text("     /__\\     ")
            center_text("    /____\\    ")
            center_text("   /______\\   ")
            center_text(" [┌ \\_  /  ┐] ")
            center_text("[ │O  \\/  O│ ]")
            center_text(" \\│    @   │/ ")
            center_text(" [@   []   @] ")
            center_text("  ──────────  ")
            center_text("   __|__|__   ")
            center_text("  /        \\  ")
            print(f"\n{user_speach}", end='')  # Show the conversation in real-time
            time.sleep(0.5)  # Shorter sleep time for smoother updates
        else:
            clear_screen()
            center_text("      \\/      ")
            center_text("      /\\      ")
            center_text("     /__\\     ")
            center_text("    /____\\    ")
            center_text("   /______\\   ")
            center_text(" [┌ \\_  /  ┐] ")
            center_text("[ │O  \\/  O│ ]")
            center_text(" \\│    @   │/ ")
            center_text(" [@  ────  @] ")
            center_text("  ──────────  ")
            center_text("   __|__|__   ")
            center_text("  /        \\  ")
            print(f"\n{user_speach}", end='')  # Show the conversation in real-time
            time.sleep(1)  # Shorter sleep time for smoother updates

            # Second frame (alternates with first frame)
            clear_screen()
            center_text("      \\/      ")
            center_text("      /\\      ")
            center_text("     /__\\     ")
            center_text("    /____\\    ")
            center_text("   /______\\   ")
            center_text(" [┌ \\_  /  ┐] ")
            center_text("[ │─  \\/  ─│ ]")
            center_text(" \\│    @   │/ ")
            center_text(" [@  ────  @] ")
            center_text("  ──────────  ")
            center_text("   __|__|__   ")
            center_text("  /        \\  ")
            print(f"\n{user_speach}", end='')  # Show the conversation in real-time
            time.sleep(0.5)  # Shorter sleep time for smoother updates

def listen():  
    # TODO: Allow user to type something for Oblo to respond to
    global user_speach
    global listening

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        listening = False

        speak(get_response('Introduce yourself very very briefly'))  # Inform the user that it's listening
        # audio = recognizer.listen(
        #     source, 
        #     timeout=None,  # No timeout, it will wait indefinitely
        #     phrase_time_limit=None  # Set a longer limit for how long it listens (10 seconds in this case)
        # )

        listening = True

        

        while True:
            if keyboard.is_pressed('ctrl+space'):
                if listening:
                    # recognizer.adjust_for_ambient_noise(source)
                    listening = False
                    speak("Go on..")  # Inform the user that it's listening
                    listening = True
                    
                    audio = recognizer.listen(
                        source, 
                        timeout=None,  # No timeout, it will wait indefinitely
                        phrase_time_limit=None  # Set a longer limit for how long it listens (10 seconds in this case)
                    )

                    time.sleep(1)
                    listening = False  # Toggle listening flag
                    
                    if user_speach != "":
                        try:                    
                            command = recognizer.recognize_google(audio)  # Recognize the user's speech
                            user_speach = f"You: {command}"  # Update the user_speach with user's input

                            # <----- COMMANDS -----> #
                            # COMMAND | PLAYING/STOPPING MUSIC
                            if "play music" in command.lower() or "stop music" in command.lower():
                                music_controller(command)

                            # COMMAND | SPOTIFY
                            # elif "entertain me" in command.lower():
                            #     speak(get_response("I will play some notes for you"))
                            #     play_midi_notes()
                            
                            # GENERAL CHAT
                            else:
                                # Get response from Gemini API
                                ai_response = get_response(command)
                                speak(ai_response)  # Speak the AI's response


                        # ERROR HANDLING
                        except sr.UnknownValueError:
                            speak(get_response('Ask the user to repeat themselves or speak clearer, very briefly'))  # Inform the user that it's listening
                            
                        except sr.RequestError:
                            speak(get_response('Tell the user something went wrong processing their sentence, very briefly'))  # Handle speech recognition errors
                    
                    listening = True
                    time.sleep(1)  # Sleep for a short time to avoid multiple toggles due to the same press
            elif keyboard.is_pressed('enter'):
                listening = False
                speak("Go on..")  # Inform the user that it's listening
                listening = True

                user_speach = "You: " 
                user_text = input("You: ")
                user_speach = f"You: {user_text}" 

                if user_text != "":
                    try:
                        # TODO: Add more fun commands
                        # <----- COMMANDS -----> #
                        # COMMAND | PLAYING/STOPPING MUSIC
                        if "play music" in user_text.lower() or "stop music" in user_text.lower():
                            music_controller(command)

                        # COMMAND | SPOTIFY
                        # elif "entertain me" in command.lower():
                        #     speak(get_response("I will play some notes for you"))
                        #     play_midi_notes()
                        
                        # GENERAL CHAT
                        else:
                            # Get response from Gemini API
                            ai_response = get_response(user_text)
                            speak(ai_response)  # Speak the AI's response

                    # ERROR HANDLING
                    except sr.UnknownValueError:
                        speak(get_response('Ask the user to repeat themselves or speak clearer, very briefly'))  # Inform the user that it's listening
                        
                    except sr.RequestError:
                        speak(get_response('Tell the user something went wrong processing their sentence, very briefly'))  # Handle speech recognition errors
                
                listening = True
                time.sleep(1)  # Sleep for a short time to avoid multiple toggles due to the same press

            time.sleep(0.1)  # Prevent high CPU usage from constant loop checking for the spacebar

def update():
    # Create separate threads for animation and listening
    anim_thread = threading.Thread(target=animate)
    anim_thread.start()  # Start the animation thread

    listen_thread = threading.Thread(target=listen)
    listen_thread.start()  # Start the listening thread

# TODO: On program end, output a text file of the conversation log
if __name__ == "__main__":
    update()
