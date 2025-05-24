from speech import listen, speak, get_response, sanitize, History, history
import keyboard
from rich.prompt import Prompt
from datetime import datetime
import whisper
import os

# base_model_path = os.path.expanduser('~\.cache\whisper/small.pt')
# base_model = whisper.load_model(base_model_path)

# from display import animate, frames
mode = 'typing'


def update():
    global command_mode
    global mode
    user_text = ""

    # if keyboard.is_pressed("t"):
    #     history.append({'role': 'instruction', 'content': "Very Briefly let user know typing mode is enabled and they can ask to switch to voice command mode later\n"})
    #     speak(get_response())
    #     mode = 'typing'
    # elif keyboard.is_pressed("s"):
    #     history.append({'role': 'instruction', 'content': "Very Briefly let user know voice command mode is enabled and they can ask to switch to type command mode later\n"})
    #     speak(get_response())
    #     mode = 'speaking'

    # if keyboard.is_pressed('space') and mode:
    #     if mode == 'speaking':
    #         user_text = listen()
        
    #     elif mode == 'typing':
    #         user_text = input()
    
    user_text = Prompt.ask('[bold blue]User[/bold blue]')
        
    if user_text:
        History.add('user', user_text)

        speak(History.add('oblo', get_response()))
        user_text = ""

    # TODO: Create separate threads for animation and listening try Curses

# TODO: On program end, output a text file of the conversation log
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    History.add('instruction', "Briefly tell the user you will begin listening to them when they press spacebar and they can press Ctrl-c to stop the program")
    speak(History.add('oblo', get_response()))
 
# , finish with 'Now, would you like typing mode (Press T), or speaking mode (Press S)' in your own way

    try:
        while True:
            update()
    except KeyboardInterrupt:
        History.add('instruction', "Say goodbye to the user very briefly")
        speak(History.add('oblo', get_response()))

        # Log Saving
        log_dir = "log"
        os.makedirs(log_dir, exist_ok=True)  # Create folder if it doesn't exist

        # Create a timestamped filename inside the log folder
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(log_dir, f"log_{timestamp}.txt")

        with open(filename, "w", encoding="utf-8") as file:
            for message in history:
                if message["role"] == "instruction":
                    continue
                role = message["role"].capitalize()
                content = message["content"]
                file.write(f"{role}: {content}\n\n")