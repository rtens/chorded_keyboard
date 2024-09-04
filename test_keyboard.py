from unittest import skip
from chorded import Keyboard

class Base:
    def setup_method(self):
        self.map = dict()
        self.written = []
        self.keyboard = Keyboard(self.map, self)

    def down(self, key):
        self.keyboard.press(key)

    def up(self, key):
        self.keyboard.release(key)

    def got(self, *writes):
        assert self.written == list(writes)

    def write(self, output):
        self.written.append(output)
                
class TestChords(Base):

    def test_only_press(self):
        self.map['L_OOOO'] = 'a'
        self.down('L')

        self.got()

    def test_unknown_chord(self):
        self.map['L_OOOO'] = 'a'
        self.down('i')
        self.up('i')

        self.got('¿')

    def test_single_keys(self):
        keys = [
            ('L', 'L_OOOO', 'a'),
            ('R', '_ROOOO', 'b'),
            ('i', '__XOOO', 'c'),
            ('m', '__OXOO', 'd'),
            ('r', '__OOXO', 'e'),
            ('p', '__OOOX', 'f'),
        ]

        for k, s, o in keys:
            self.map[s] = o
            self.down(k)
            self.up(k)

        self.got('a', 'b', 'c', 'd', 'e', 'f')

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

    def test_stuck_key(self):
        self.map['L_XOOO'] = 'a'
        self.map['__XOOO'] = 'x'
        self.down('L')
        self.down('i')
        self.up('L')
        self.down('i')
        self.up('i')

        self.got('a')

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

class TestModifiers(Base):

    def test_just_modifier(self):
        self.map['c__OOOO'] = 'a'
        self.down('ctrl')
        self.up('ctrl')

        self.got('a')

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

class TestModes(Base):

    def test_unknown_chord(self):
        self.map['L_OOOO'] = '::foo'
        self.down('L')
        self.up('L')
        self.down('i')
        self.up('i')

        self.got('¿')

    def test_chord_in_mode(self):
        self.map['L_OOOO'] = '::foo'
        self.map['(foo)__XOOO'] = 'a'
        self.down('L')
        self.up('L')
        self.down('i')
        self.up('i')

        self.got('a')

    def test_leave_mode_after_chord(self):
        self.map['L_OOOO'] = '::foo'
        self.map['(foo)__XOOO'] = 'a'
        self.map['__XOOO'] = 'b'
        self.down('L')
        self.up('L')
        self.down('i')
        self.up('i')
        self.down('i')
        self.up('i')

        self.got('a', 'b')
        
    def test_leave_mode_after_unknown(self):
        self.map['L_OOOO'] = '::foo'
        self.map['__XOOO'] = 'a'
        self.down('L')
        self.up('L')
        self.down('i')
        self.up('i')
        self.down('i')
        self.up('i')

        self.got('¿', 'a')
        
