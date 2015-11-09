#!/usr/bin/python

import sys, math, cmath, itertools, functools
import commands

def NinetyNineBottles():
    x = 99
    for i in range(99):
        w = 'Take one down and pass it around, '+str((x-(i+1)))+' bottle of beer on the wall.'
        y = str((x-i))+' bottles of beer on the wall, '+str((x-i))+' bottles of beer'
        z = 'Go to the Store and buy some more, '+str(x)+' bottle of beer on the wall.'
        if i == (x-1):
            print(y + '\n' + z)
        else:
            print(y + '\n' + w)
        i += 1

class SeriousFunction(object):
    def __init__(self, code, srs):
        self.srs = srs
        self.code = code
    def __call__(self):
        self.srs.eval(self.code)
    def __str__(self):
        return '`%s`'%code
    def __repr__(self):
        self.__call__()

class Seriously(object):
    def __init__(self):
        self.stack = []
        self.fn_table = commands.fn_table
    def push(self,val):
        self.stack=[val]+self.stack
    def pop(self):
        return self.stack.pop(0)
    def append(self, val):
        self.stack+=[val]
    def eval(self, code):
        i=0
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
                v = ''
                i+=1
                while i<len(code) and code[i]!=':':
                    v+=code[i]
                    i+=1
                self.push(int(v))
            elif c == 'W':
                inner = ''
                i+=1
                while i<len(code) and code[i]!='W':
                    inner+=code[i]
                    i+=1
                while self.stack[0]:
                    self.eval(inner)
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
                self.push(SeriousFunction(f))
            elif c == 'Q' and len(self.stack) == 0:
                print code
            elif ord(c) in range(48,58):
                self.push(int(c))
            elif c == 'H' and len(self.stack) == 0:
                print 'Hello, World!'
            elif c == 'N' and len(self.stack) == 0:
                print NinetyNineBottles()
            elif ord(c) == 130:
                self.stack = []
            else:
                old_stack = self.stack[:]
                try:
                    self.fn_table.get(ord(c), lambda x:x)(self)
                except:
                    self.stack = old_stack[:]
            i+=1

if __name__ == '__main__':
    srs = Seriously()
    if len(sys.argv) < 2:
        while 1:
            try:
                srs.eval(raw_input('>>> '))
            except EOFError:
                exit()
            finally:
                print
                print srs.stack
    else:
        if sys.argv[1] == '-c':
            srs.eval(sys.argv[2])
        else:
            with open(sys.argv[2]) as f:
                srs.eval(f.read())