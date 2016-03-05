#!/usr/bin/python3
import argparse
import ast
import binascii
import hashlib
import random
import re
import readline
import sys
import traceback
import SeriouslyCommands
from lib.cp437 import CP437

anytype = SeriouslyCommands.anytype

ord_cp437 = CP437.ord

chr_cp437 = CP437.chr

class Seriously(object):
    @classmethod
    def _make_new(cls,init_stack=[], debug_mode=False):
        return cls(init_stack, debug_mode)
    def make_new(self,*stack):
        return self._make_new(init_stack=list(stack), debug_mode=self.debug_mode)
        return res
    def __init__(self, init_stack=[], debug_mode=False, hex_mode=False):
        self.stack = init_stack
        self.debug_mode=debug_mode
        self.fn_table = SeriouslyCommands.fn_table
        self.code = ''
        self.hex_mode = hex_mode
        self.preserve = False
        self.pop_counter = 0
    def push(self,val):
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
        self.stack[:] = [val] + self.stack
    def toggle_preserve(self):
        self.preserve = not self.preserve
    def eval(self, code):
        if self.hex_mode:
            tmp = ''
            for i in range(0, len(code), 2):
                tmp += chr_cp437(int(code[i:i+2], 16))
            code = tmp
        if self.debug_mode:
            print(code)
        i=0
        self.code = code
        while i < len(code):
            old_stack = self.stack[:]
            try:
                c = code[i]
                if c == '"':
                    s = ""
                    i+=1
                    while i<len(code) and code[i]!='"':
                        s+=code[i]
                        i+=1
                    self.push(s)
                elif c == "'":
                    i+=1
                    self.push(code[i])
                elif c == ':':
                    v = ""
                    i+=1
                    while i<len(code) and code[i] in '0123456789.ij+-':
                        v+=code[i]
                        i+=1
                    i-=1
                    val = 0
                    try:
                        val = eval(v)
                    except:
                        pass
                    val = val if anytype(val, int, float, complex) else 0
                    self.push(val)
                elif c == 'W':
                    inner = ''
                    i+=1
                    while i<len(code) and code[i]!='W':
                        inner+=code[i]
                        i+=1
                    if self.debug_mode:
                        print("while loop code: %s"%inner)
                    while self.peek():
                        self.eval(inner, print_at_end=False)
                elif c == '[':
                    l = ''
                    i+=1
                    while i<len(code) and code[i]!=']':
                        l+=code[i]
                        i+=1
                    self.push(eval('[%s]'%l))
                elif c == '`':
                    f = ''
                    i+=1
                    while i<len(code) and code[i]!='`':
                        f+=code[i]
                        i+=1
                    self.push(SeriouslyCommands.SeriousFunction(f))
                elif ord(c) in range(48,58):
                    self.push(int(c))
                else:
                    if self.debug_mode:
                        print(binascii.hexlify(chr(ord_cp437(c)).encode()).decode().upper())
                    self.fn_table.get(ord_cp437(c), lambda x:x)(self)
                    if self.debug_mode:
                        print(self.stack)
            except SystemExit:
                exit()
            except KeyboardInterrupt:
                exit()
            except:
                if self.debug_mode:
                    traceback.print_exc()
                self.stack = old_stack[:]
            finally:
                i+=1
        return self.stack


def srs_exec(debug_mode=False, file_obj=None, code=None, hex=False):
    srs = Seriously(debug_mode=debug_mode, hex_mode=hex)
    if file_obj:
        for x in srs.eval(file_obj.read()):
            print(x)
        file_obj.close()
    else:
        for x in srs.eval(code):
            print(x)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the Seriously interpreter")
    parser.add_argument("-d", "--debug", help="turn on debug mode", action="store_true")
    parser.add_argument("-q", "--quiet", help="turn off REPL prompts and automatic stack printing, only print code STDOUT output", action="store_true")
    parser.add_argument("-x", "--hex", help="turn on hex mode (code is taken in hex values instead of binary bytes)", action="store_true")
    parser.add_argument("-i", "--ide", help="turn on IDE mode, which disables unsafe commands", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--code", help="run the specified code")
    group.add_argument("-f", "--file", help="specify an input file", type=argparse.FileType('r'))
    args = parser.parse_args()
    if args.ide:
        commands.fn_table[0xF0] = lambda x: x.push(ast.literal_eval(x.pop()))
    srs_exec(args.debug, args.file, args.code, args.hex)
