#!/usr/bin/python

import sys, math, cmath, itertools, functional

class SeriousFunction(object):
    def __init__(self, code, srs):
        self.srs = srs
        self.code = code
    def __call__(self):
        self.srs.eval(self.code)
    def __repr__(self):
        return '`%s`'%code

class Seriously(object):
    def __init__(self):
        self.stack = []
        self.fn_table = {127:exit}
    def push(self,val):
        self.stack=[val]+self.stack
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
                self.push(int(s))
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
                self.push(l)
            elif c == '`':
                f = ''
                i+=1
                while i<len(code) and code[i]!='`':
                    f+=code[i]
                    i+=1
                self.push(SeriousFunction(f))
            else:
                self.fn_table.get(ord(c), lambda:pass)()
            i+=1

if __name__ == '__main__':
    srs = Seriously()
    while 1:
        srs.eval(raw_input('>>> '))
        print srs.stack