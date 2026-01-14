from pynput import keyboard
import time

running = True

player_x = 10
player_y = 10

npc_x = 50
npc_y = 50
npc_dir_x = 1   # 1 = right, -1 = left
npc_dir_y = 1 

x_min = 0
x_max = 100
y_min = 0
y_max = 100


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
            self.pressed.discard(ch)
        except AttributeError:
            pass

    def __init__(self):
        self.pressed = set()
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        listener.start()


kb = KBPoller()


def scan_keys():
    if "q" in kb.pressed:
        return "q"
    for ch in ("a", "d", "w", "s"):
        if ch in kb.pressed:
            return ch
    return None


def render_state():
    print(
        f"player: ({player_x}, {player_y}) , "
        f"npc: ({npc_x}, {npc_y})"
    )


def update_state(inp):
    global player_x, player_y, running
    global npc_x, npc_y, npc_dir_x, npc_dir_y

    if inp == "a":
        player_x -= 1
    elif inp == "d":
        player_x += 1
    elif inp == "w":
        player_y -= 1
    elif inp == "s":
        player_y += 1
    elif inp == "q":
        running = False

    player_x = max(x_min, min(x_max, player_x))
    player_y = max(y_min, min(y_max, player_y))

    npc_x += 1 * npc_dir_x
    npc_y += 2 * npc_dir_y

    if npc_x <= x_min or npc_x >= x_max:
        npc_dir_x *= -1
        npc_x = max(x_min, min(x_max, npc_x))

    if npc_y <= y_min or npc_y >= y_max:
        npc_dir_y *= -1
        npc_y = max(y_min, min(y_max, npc_y))


while running:
    render_state()
    inp = scan_keys()
    update_state(inp)
    time.sleep(1/30)