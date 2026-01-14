from pynput import keyboard
import time

class KBPoller:
    def on_press(self, key):
        try:
            ch = key.char.lower()
            self.pressed.add(ch)
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            ch = key.char.lower()
            self.pressed.remove(ch)
        except AttributeError:
            pass

    def __init__(self):
        self.pressed = set()

        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release, suppress=True)
        listener.start()

kb = KBPoller()

running = True

player_x = 10
player_y = 10

x_min = 0
x_max = 100
y_min = 0
y_max = 100

def scan_keys():
    return kb.pressed

def render_state():
    print("player is at:", player_x, player_y)

def update_state(inp):
    global player_x, player_y, running
    if "a" in inp:
        player_x -= 1
    elif "d" in inp:
        player_x += 1
    elif "w" in inp:
        player_y -= 1
    elif "s" in inp:
        player_y += 1
    elif "q" in inp:
        running = False

    if player_x < x_min:
        player_x = x_min
    if player_x > x_max:
        player_x = x_max
    if player_y < y_min:
        player_y = y_min
    if player_y > y_max:
        player_y = y_max

while running:
    # read/check for user actions (input)
    # update game state (physics, AI, etc)
    # render game state (graphics)

    render_state()
    inp = scan_keys()

    update_state(inp)
    time.sleep(0.1)