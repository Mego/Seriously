#!/usr/bin/env python3
import sys
if sys.version_info[0] != 3:
    print("You must use Python 3 to run this script!")
    exit()

import argparse
from ast import literal_eval
import binascii
import hashlib
import random
import re
import readline
import traceback
from . import SeriouslyCommands
from lib.cp437 import CP437
from lib.iterable import deque, as_list

anytype = SeriouslyCommands.anytype

ord_cp437 = CP437.ord

chr_cp437 = CP437.chr


class Seriously(object):
    @classmethod
    def _make_new(cls, init=None, debug_mode=False):
        return cls([] if init is None else init, debug_mode)

    def make_new(self, *stack):
        return self._make_new(init=list(stack), debug_mode=self.debug_mode)

    def __init__(self, init_stack=None, debug_mode=False):
        self.stack = deque(init_stack if init_stack is not None else [])
        self.debug_mode = debug_mode
        self.code = ''
        self.fn_table = SeriouslyCommands.fn_table
        self.preserve = False
        self.pop_counter = 0

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        return self.stack.pop() if not self.preserve else self.preserve_pop()

    def preserve_pop(self):
        v = self.stack.pop()
        self.push(v)
        return v

    def peek(self):
        return self.stack[-1] if self.stack else None

    def prepend(self, val):
        self.stack.appendleft(val)

    def toggle_preserve(self):
        self.preserve = not self.preserve

    def clear_stack(self):
        self.stack.clear()

    def eval(self, code):
        if self.debug_mode:
            print(code)
        i = 0
        if all(x not in code for x in (',',chr_cp437(0xCA),chr_cp437(0x09),chr_cp437(0x0C))):
            for line in sys.stdin.read().splitlines():
                self.push(literal_eval(line))
        self.code = code
        while i < len(code):
            old_stack = self.stack.copy()
            try:
                c = code[i]
                if c == '"':
                    s = ""
                    i += 1
                    while i < len(code) and code[i] != '"':
                        s += code[i]
                        i += 1
                    self.push(s)
                elif c == "'":
                    i += 1
                    self.push(code[i])
                elif c == ':':
                    v = ""
                    i += 1
                    while i < len(code) and code[i] in '0123456789.ij+-':
                        v += code[i]
                        i += 1
                    i -= 1
                    val = 0
                    v = v.replace('i', 'j')
                    if self.debug_mode:
                        print(v)
                    try:
                        val = literal_eval(v)
                        if self.debug_mode:
                            print(val)
                    except:
                        if self.debug_mode:
                            print("Failed to eval numeric")
                    val = val if anytype(val, int, float, complex) else 0
                    self.push(val)
                elif c == 'W':
                    inner = ''
                    i += 1
                    while i < len(code) and code[i] != 'W':
                        inner += code[i]
                        i += 1
                    if self.debug_mode:
                        print("while loop code: {}".format(inner))
                    while self.peek():
                        self.eval(inner)
                elif c == '[':
                    l = ''
                    i += 1
                    nest = 1
                    while i < len(code):
                        if code[i] == '[':
                            nest += 1
                        elif code[i] == ']':
                            nest -= 1
                            if nest == 0:
                                break
                        l += code[i]
                        i += 1
                    self.push(literal_eval('[{}]'.format(l)))
                    if self.debug_mode:
                        print("list: [{}]".format(l))
                        print(self.stack)
                elif c == '`':
                    f = ''
                    i += 1
                    while i < len(code) and code[i] != '`':
                        f += code[i]
                        i += 1
                    if self.debug_mode:
                        print('fn: {}'.format(f))
                    self.push(SeriouslyCommands.SeriousFunction(f))
                elif ord(c) in range(48, 58):
                    self.push(int(c))
                elif ord_cp437(c) == 0x0B:
                    i += 1
                    self.push(SeriouslyCommands.SeriousFunction(code[i]))
                    self.fn_table.get(ord_cp437('M'))(self)
                else:
                    if self.debug_mode:
                        print("{:2X}".format(ord_cp437(c)))
                    self.fn_table.get(ord_cp437(c), lambda x: x)(self)
                    if self.debug_mode:
                        print(self.stack)
            except SystemExit:
                exit()
            except KeyboardInterrupt:
                exit()
            except:
                if self.debug_mode:
                    traceback.print_exc()
                self.stack = old_stack
            finally:
                i += 1
        return as_list(self.stack)[::-1]


def srs_exec(debug_mode=False, file_obj=None, code=None):
    srs = Seriously(debug_mode=debug_mode)
    if file_obj:
        for x in srs.eval(file_obj.read()):
            print(x)
        file_obj.close()
    else:
        for x in srs.eval(code):
            print(x)


def ide_mode():
    SeriouslyCommands.fn_table[0xF0] = lambda x: x.push(literal_eval(x.pop()))

def main():
    parser = argparse.ArgumentParser(
                description="Run the Seriously interpreter")
    parser.add_argument("-d", "--debug", help="turn on debug mode",
                        action="store_true")
    parser.add_argument("-i", "--ide",
                        help="disable unsafe commands", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--code", help="run the specified code")
    group.add_argument("-f", "--file", help="specify an input file",
                       type=argparse.FileType('r'))
    args = parser.parse_args()
    if args.ide:
        ide_mode()
    srs_exec(args.debug, args.file, args.code)
    
if __name__ == '__main__':
    main()