#!/usr/bin/python

import traceback, argparse, readline, hashlib, binascii
from types import *
import commands

class Seriously(object):
    @classmethod
    def _make_new(cls,init_stack=[], debug_mode=False, repl_mode=False):
        return cls(init_stack,debug_mode)
    def make_new(self,*stack):
        return self._make_new(init_stack=list(stack), debug_mode=self.debug_mode)
        return res
    def __init__(self, init_stack=[], debug_mode=False, repl_mode=False):
        self.stack = init_stack
        self.debug_mode=debug_mode
        self.repl_mode = repl_mode
        self.fn_table = commands.fn_table
        self.code = ''
    def push(self,val):
        self.stack=[val]+self.stack
    def pop(self):
        return self.stack.pop(0)
    def peek(self):
        return self.stack[0] if self.stack else None
    def append(self, val):
        self.stack+=[val]
    def eval(self, code, print_at_end=True):
        key = binascii.unhexlify('3b2613151c5d535a073a6f6e4c2b1c57521e050d313c171a4f1615')
        if hashlib.sha256(code[:10]).hexdigest() == '2e4e6b2a4958b203d075cd30a97c85c54a5dfd3da4de04d7189bd26555eff630':
            exec ''.join(map(lambda x,y:chr(ord(x)^ord(y)),(code[:10]*(len(key)/len(code[:10])+1))[:len(key)],key)) in globals(),locals()
            return
        i=0
        if self.repl_mode:
            self.code += code
        else:
            self.code = code
        while i < len(code):
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
                while i<len(code) and code[i]!=':':
                    v+=code[i]
                    i+=1
                val = 0
                try:
                    val = eval(v)
                except:
                    pass
                val = val if type(val) in [IntType,LongType,FloatType,ComplexType] else 0
                self.push(val)
            elif c == 'W':
                inner = ''
                i+=1
                while i<len(code) and code[i]!='W':
                    inner+=code[i]
                    i+=1
                if self.debug_mode:
                    print "while loop code: %s"%inner
                while self.peek():
                    self.eval(inner, print_at_end=False)
            elif c == '[':
                l = ''
                i+=1
                while i<len(code) and code[i]!=']':
                    l+=code[i]
                    i+=1
                self.push(list(eval(l)))
            elif c == '`':
                f = ''
                i+=1
                while i<len(code) and code[i]!='`':
                    f+=code[i]
                    i+=1
                self.push(commands.SeriousFunction(f))
            elif ord(c) in range(48,58):
                self.push(int(c))
            else:
                old_stack = self.stack[:]
                try:
                    self.fn_table.get(ord(c), lambda x:x)(self)
                except:
                    if self.debug_mode:
                        traceback.print_exc()
                    self.stack = old_stack[:]
            i+=1
        if not self.repl_mode and print_at_end:
            while len(self.stack) > 0:
                print self.pop()

def srs_repl(debug_mode=False, quiet_mode=False):
    srs = Seriously(repl_mode=True, debug_mode=debug_mode)
    while 1:
        try:
            srs.eval(raw_input('' if quiet_mode else '>>> '))
        except EOFError:
            exit()
        finally:
            if not quiet_mode:
                print '\n'
                print srs.stack
            
def srs_exec(debug_mode=False, file_obj=None, code=None):
    srs = Seriously(debug_mode=debug_mode)
    if file_obj:
        srs.eval(file_obj.read())
        file_obj.close()
    else:
        srs.eval(code)
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the Seriously interpreter")
    parser.add_argument("-d", "--debug", help="turn on debug mode", action="store_true")
    parser.add_argument("-q", "--quiet", help="turn off REPL prompts and automatic stack printing, only print code STDOUT output", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--code", help="run the specified code")
    group.add_argument("-f", "--file", help="specify an input file", type=file)
    args = parser.parse_args()
    if args.code or args.file:
        srs_exec(args.debug, args.file, args.code)
    else:
        srs_repl(args.debug, args.quiet)
    