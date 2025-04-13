from speech import listen, speak, get_response, sanitize
import keyboard

def update():
    user_text = ""

    if keyboard.is_pressed('space'):
        user_text = listen()
    
    if user_text:
        speak(get_response(user_text) )
        user_text = ""


    # Create separate threads for animation and listening
    # anim_thread = threading.Thread(target=animate)
    # anim_thread.start()  # Start the animation thread

    # listen_thread = threading.Thread(target=listen)
    # listen_thread.start()  # Start the listening thread

# TODO: On program end, output a text file of the conversation log
if __name__ == "__main__":
    speak(get_response("Tell the user you will begin listening to them when they press spacebar and they can press Ctrl-c to stop the program"))

    try:
        while True:
            update()
    except KeyboardInterrupt:
        speak(get_response("Say goodbye to the user very briefly"))
        