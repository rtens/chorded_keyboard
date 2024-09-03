import keyboard
import json

from chorded import Keyboard

class Out:
    def write(self, output):
        print(">>>", output, flush=True)
        if len(output) == 1:
            keyboard.write(output)
        elif output:
            keyboard.send(output)

with open('map.json') as f:
    map = json.load(f)

chorded = Keyboard(map, Out())

keys = {
    "q": "win",
    "w": "alt",
    "e": "ctrl",
    "r": "shift",
    "v": "L",
    "b": "R",
    "u": "i",
    "i": "m",
    "o": "r",
    "p": "p"
}

active = False
def on_key(event):
    global active
    if active:
        return
    
    key = keys[event.name]
    pressed = event.event_type == keyboard.KEY_DOWN

    active = True
    if pressed:
        chorded.press(key)
    else:
        chorded.release(key)
    active = False

    print(event.event_type, key, chorded.pressed, chorded.loaded, flush=True)

for k in keys.keys():
    keyboard.hook_key(k, on_key, suppress=True)
    
keyboard.wait('esc', suppress=True)
