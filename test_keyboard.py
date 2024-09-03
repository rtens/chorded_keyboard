from unittest import skip
from chorded import Keyboard

class Base:
    def setup_method(self):
        self.map = dict()
        self.out = Out()
        self.keyboard = Keyboard(self.map, self.out)

    def down(self, key):
        self.keyboard.press(key)

    def up(self, key):
        self.keyboard.release(key)

    def got(self, *writes):
        assert self.out.written == list(writes)

class Out:
    def __init__(self):
        self.written = []

    def write(self, output):
        self.written.append(output)
                
class TestSingleKeys(Base):

    def test_only_press(self):
        self.map['L_OOOO'] = 'a'
        self.down('L')

        self.got()

    def test_unknown_chord(self):
        self.map['L_OOOO'] = 'a'
        self.down('i')
        self.up('i')

        self.got()

    def test_single_keys(self):
        keys = [
            ('L', 'L_OOOO'),
            ('R', '_ROOOO'),
            ('i', '__XOOO'),
            ('m', '__OXOO'),
            ('r', '__OOXO'),
            ('p', '__OOOX'),
        ]

        for k, s in keys:
            self.out.written.clear()
            self.map.clear()
            self.map[s] = 'a' + k
            self.down(k)
            self.up(k)

            self.got('a' + k)

    def test_repeated_keys(self):
        self.map['__XOOO'] = 'a'
        self.down('i')
        self.up('i')
        self.down('i')
        self.up('i')

        self.got('a', 'a')

    def test_multiple_keys(self):
        self.map['LROOOO'] = 'a'
        self.down('L')
        self.down('R')
        self.up('R')

        self.got('a')

    def test_release_all_keys(self):
        self.map['LROOOO'] = 'a'
        self.down('L')
        self.down('R')
        self.up('R')
        self.up('L')

        self.got('a')

    def test_flicker_key(self):
        self.map['L_XOOO'] = 'a'
        self.map['L_OXOO'] = 'b'
        self.down('L')
        self.down('i')
        self.up('i')
        self.down('m')
        self.up('m')

        self.got('a', 'b')

    def test_ignore_invalid_release(self):
        self.map['__XOOO'] = 'x'
        self.down('i')
        self.up('m')

        self.got()

    def test_shift_one(self):
        self.map['s__XOOO'] = 'a'
        self.down('shift')
        self.down('i')
        self.up('i')

        self.got('a')

    def test_shift_many(self):
        self.map['s__XOOO'] = 'a'
        self.map['s__OXOO'] = 'b'
        self.down('shift')
        self.down('i')
        self.up('i')
        self.down('m')
        self.up('m')

        self.got('a', 'b')

    def test_unshift(self):
        self.map['s__XOOO'] = 'a'
        self.map['__XOOO'] = 'b'
        self.down('shift')
        self.down('i')
        self.up('i')
        self.up('shift')
        self.down('i')
        self.up('i')

        self.got('a', 'b')

class TestModalCombinations(Base):

    def test_shift(self):
        self.map['__XOOO'] = 'a'
        self.down('shift')
        self.down('i')
        self.up('i')

        self.got('shift+a')

    def test_others(self):
        self.map['__XOOO'] = 'a'
        self.down('windows')
        self.down('alt')
        self.down('ctrl')
        self.down('i')
        self.up('i')

        self.got('windows+alt+ctrl+a')

    def test_ctrl_and_shift(self):
        self.map['__XOOO'] = 'a'
        self.down('ctrl')
        self.down('shift')
        self.down('i')
        self.up('i')

        self.got('ctrl+shift+a')

    def test_ctrl_shifted(self):
        self.map['s__XOOO'] = 'a'
        self.down('ctrl')
        self.down('shift')
        self.down('i')
        self.up('i')

        self.got('ctrl+a')

