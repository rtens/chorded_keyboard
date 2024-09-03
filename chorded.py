
class Keyboard:
    def __init__(self, map, out):
        self.map = map
        self.out = out
        self.pressed = set()
        self.loaded = False

    def press(self, key):
        self.loaded = True
        self.pressed.add(key)

    def release(self, key):
        if key not in self.pressed:
            return
        
        if self.loaded:
            self.shoot()
        self.loaded = False

        self.pressed.remove(key)

    def shoot(self):
        for split in [0, 3, 4]:
            modifiers = [k for k, y, n in strings[0:split]
                         if k in self.pressed]
            
            chord = "".join([y if k in self.pressed else n
                             for k, y, n in strings[split:]])

            if chord in self.map:
                self.out.write('+'.join(modifiers + [self.map[chord]]))
                return


strings = [
    ('windows', 'w', ''),
    ('alt', 'a', ''),
    ('ctrl', 'c', ''),
    ('shift', 's', ''),
    ('L', 'L', '_'),
    ('R', 'R', '_'),
    ('i', 'X', 'O'),
    ('m', 'X', 'O'),
    ('r', 'X', 'O'),
    ('p', 'X', 'O'),
]

