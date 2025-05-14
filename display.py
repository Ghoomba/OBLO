import time
import os
from speech import user_text

# Load file
with open("animations/laughing.txt", "r", encoding="utf-8") as animations:
    lines = animations.read().splitlines()

# Frame height (number of lines per frame)
frame_height = 12

# Split into frames
frames = [lines[i:i+frame_height] for i in range(0, len(lines), frame_height)]

# Clear the terminal screen (works for Windows and Unix-based systems)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate(frame):
    clear_screen()  # Clear terminal
    print("\n".join(frame))
    time.sleep(0.5)
    
        
        