from speech import listen, speak, get_response, sanitize
import keyboard
# from display import animate, frames
mode = ''
def update():
    global command_mode
    global mode
    user_text = ""

    if keyboard.is_pressed("t"):
        speak(get_response("Very Briefly let user know typing mode is enabled and they can ask to switch to voice command mode later"))
        mode = 'typing'
    elif keyboard.is_pressed("s"):
        speak(get_response("Very Briefly let user know voice command mode is enabled and they can ask to switch to type command mode later"))
        mode = 'speaking'

    if keyboard.is_pressed('space') and mode:
        if mode == 'speaking':
            user_text = listen()
        
        elif mode == 'typing':
            user_text = input()
    
    if user_text:
        
        speak(get_response(user_text))
        user_text = ""

        # for frame in frames: 
        #     # animate(frame)
        #     speak(get_response(user_text))
        #     user_text = ""

    # TODO: Create separate threads for animation and listening

# TODO: On program end, output a text file of the conversation log
if __name__ == "__main__":
    speak(get_response("Briefly tell the user you will begin listening to them when they press spacebar and they can press Ctrl-c to stop the program, finish with 'Now, would you like typing mode (Press T), or speaking mode (Press S)' in your own way"))

    try:
        while True:
            update()
    except KeyboardInterrupt:
        speak(get_response("Say goodbye to the user very briefly"))
        