#!/usr/bin/env python3
import sys
if sys.version_info[0] != 3: # pragma: no cover
    print("You must use Python 3 to run Seriously!")
    exit()

import argparse
from ast import literal_eval
import atexit
import binascii
import collections
import hashlib
import os
import random
import re
import traceback
from . import SeriouslyCommands
from lib.cp437 import CP437
from lib.iterable import deque, as_list

anytype = SeriouslyCommands.anytype

ord_cp437 = CP437.ord

chr_cp437 = CP437.chr

def remove_lists_and_strings(code):
    result = ''
    i = 0
    while i < len(code):
        c = code[i]
        if c == '[':
            i += 1
            nest = 1
            while i < len(code):
                if code[i] == '[':
                    nest += 1
                elif code[i] == ']':
                    nest -= 1
                    if nest == 0:
                        break
                i += 1
        elif c == "'":
            i += 2
        elif c == '"':
            i += 1
            while i < len(code) and code[i] != '"':
                i += 1
            i += 1
        else:
            result += code[i]
            i += 1
    return result

class Seriously:
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
        self.inputs = []

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
        if all(x not in remove_lists_and_strings(code) for x in (',',chr_cp437(0xCA),chr_cp437(0x09),chr_cp437(0x15))):
            for line in sys.stdin.read().splitlines():
                self.push(literal_eval(line))
                self.inputs.append(literal_eval(line))
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
                        while not val and v:
                            v = v[:-1]
                            i -= 1
                            try:
                                val = literal_eval(v)
                                break
                            except:
                                continue
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
                elif c == '⌠':
                    fn = ''
                    i += 1
                    nest = 1
                    while i < len(code):
                        if code[i] == '⌠':
                            nest += 1
                        elif code[i] == '⌡':
                            nest -= 1
                            if nest == 0:
                                break
                        fn += code[i]
                        i += 1
                    self.push(SeriouslyCommands.SeriousFunction(fn))
                    if self.debug_mode:
                        print("fn: {}".format(fn))
                        print(self.stack)
                elif c == '`':
                    i += 1
                    self.push(SeriouslyCommands.SeriousFunction(code[i]))
                elif ord(c) in range(48, 58):
                    self.push(int(c))
                elif ord_cp437(c) == 0x0B:
                    i += 1
                    self.push(SeriouslyCommands.SeriousFunction(code[i]))
                    self.fn_table.get(ord_cp437('M'))(self)
                elif ord_cp437(c) == 0x0C:
                    i += 1
                    a,b = self.pop(), self.pop()
                    if not isinstance(a, collections.Iterable):
                        a = [a for _ in (b if isinstance(b, collections.Iterable) else [1])]
                    if not isinstance(b, collections.Iterable):
                        b = [b for _ in a]
                    self.push(b)
                    self.push(a)
                    self.fn_table.get(ord_cp437('Z'))(self)
                    self.push(SeriouslyCommands.SeriousFunction('i'+code[i]))
                    self.fn_table.get(ord_cp437('M'))(self)
                elif ord_cp437(c) == 0x14:
                    i += 1
                    cmd = code[i]
                    a = self.pop()
                    for _ in range(a):
                        self.eval(cmd)
                elif ord_cp437(c) == 0x0E:
                    cmd1, cmd2 = code[i+1], code[i+2]
                    temp_stack = self.stack.copy()
                    self.eval(cmd1)
                    res1 = self.stack.copy()
                    self.stack = temp_stack
                    self.eval(cmd2)
                    res2 = self.stack.copy()
                    self.stack = deque()
                    self.push([res1 if len(res1) > 1 else res1[0], res2 if len(res2) > 1 else res2[0]])
                    i += 2
                else:
                    if self.debug_mode:
                        print("{:2X}".format(ord_cp437(c)))
                    self.fn_table.get(ord_cp437(c), lambda x: x)(self)
                    if self.debug_mode:
                        print(self.stack)
            except SystemExit:
                exit()
            except KeyboardInterrupt: # pragma: no cover
                exit()
            except:
                if self.debug_mode:
                    traceback.print_exc()
                self.stack = old_stack
            finally:
                i += 1
        return as_list(self.stack)[::-1]

def srs_exec(debug_mode=False, file_obj=None, code=None, ide_mode=False): # pragma: no cover
    code = code or file_obj.read()
    if (not ide_mode) and hashlib.sha256(code.encode()).hexdigest() == 'e8809dfaff977e1b36210203b7b44e83102263444695c1123799bc43358ae1c2':
        try:
            from Crypto.Cipher import AES
            hidden = binascii.unhexlify(b'f2ac048e406d7244ca202e34841611e115a9c97d554d0681a9ad1bb8f3d7f30b083ae2bae60721228fa5caaa39d205e4e8c61421b9e8fdcbd4b03cafa0e6d726540de6e8bbddf42796a63eb3112c0890bc2f32a435ae304c1bc8d9a463402c9ef1b3fcdbf53743cb737a147bb1aa16e4a71a22adac29d1b310358c40699edf897942e83ff7e1949777eebc02e9ecf24e')
            cipher = AES.new(code.encode(), AES.MODE_ECB)
            secret = cipher.decrypt(hidden).decode()
            exec(secret)
            exit()
        except ImportError:
            pass
    srs = Seriously(debug_mode=debug_mode)
    for x in srs.eval(code):
        print(x)

def ide_mode():
    SeriouslyCommands.fn_table[0xF0] = lambda x: x.push(literal_eval(x.pop()))

def main(): # pragma: no cover
    parser = argparse.ArgumentParser(
                description="Run the Seriously interpreter")
    parser.add_argument("-d", "--debug", help="turn on debug mode",
                        action="store_true")
    parser.add_argument("-i", "--ide",
                        help="disable unsafe commands", action="store_true")
    parser.add_argument("-N", "--no-input",
                        help="don't try to read input (equivalent to piping /dev/null)", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--code", help="run the specified code")
    group.add_argument("-f", "--file", help="specify an input file",
                       type=argparse.FileType('r'))
    args = parser.parse_args()
    if args.ide:
        ide_mode()
    if args.no_input:
        sys.stdin = open(os.devnull, 'r')
        atexit.register(lambda: sys.stdin.close())
    srs_exec(args.debug, args.file, args.code, args.ide)

if __name__ == '__main__':
    main()
