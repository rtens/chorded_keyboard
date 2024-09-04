
class Keyboard:
    def __init__(self, map, out):
        self.map = map
        self.out = out
        self.pressed = set()
        self.loaded = False
        self.mode = None

    def press(self, key):
        if key in self.pressed:
            return
        
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
        mapped = self.map_chord()
        self.mode = None

        if not mapped:
            self.out.write('¿')
        
        elif mapped.startswith('::'):
            self.mode = mapped[2:]

        else:
            self.out.write(mapped)
        

    def map_chord(self):
        for split in [0, 3, 4]:
            modifiers = [k for k, y, n in strings[0:split]
                         if k in self.pressed]

            if self.mode:
                mode = '(' + self.mode + ')'
            else:
                mode = ''
            
            chord = mode + "".join(
                [y if k in self.pressed else n
                 for k, y, n in strings[split:]]
            )

            if chord in self.map:
                return '+'.join(modifiers + [self.map[chord]])


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

