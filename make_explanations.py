#!/usr/bin/env python

def make_explanations():
    lines = []
    with open('commands.txt','Urb') as f:
        lines = f.read().split('\n')[:256]
    ex = "var explanations = {\n%s\n};"
    exps = []
    for line in lines:
        toks = line.split(':')
        val,desc = toks[0],':'.join(toks[1:])
        val = val[:val.index(' ')]
        desc = repr(desc.strip())
        exps.append('"%s":%s'%(val,desc))
    with open('static/explanations.js','wb') as f:
        f.write(ex%(',\n'.join(exps)))
        
if __name__ == '__main__':
    make_explanations()