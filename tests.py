#!/usr/bin/env python3
from lib.cp437 import CP437

if __name__ == '__main__':
    assert CP437.ord('a') == ord('a')
    assert CP437.ord('φ') == 0xED
    assert CP437.chr(ord('A')) == 'A'
    assert CP437.chr(0xE3) == 'π'
    assert CP437.from_Unicode('abcd') == [ord(c) for c in 'abcd']
    assert CP437.from_Unicode('αß') == [0xE0, 0xE1]
    assert CP437.from_Unicode('¤') == [0xC2, 0xA4]
