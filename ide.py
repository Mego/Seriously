#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import print_function
from flask import Flask, render_template, url_for, request
from subprocess import Popen, PIPE, check_call
import os, string
from itertools import *

app = Flask(__name__)

cp437table = ''.join(map(chr,range(128))) + u"ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ "

def ord_cp437(c):
    return cp437table.index(c)
    
def chr_cp437(o):
    return cp437table[o]
    
def srs_run(hex_code):
    print('Got code:', hex_code, 'input:', input_str)
    print('Running Seriously code...')
    p = Popen(['./seriously.py', '-q', '-x', '-c', hex_code], stdout=PIPE, stderr=PIPE, stdin=PIPE)
    output, error = map(lambda s: s.decode('utf-8'), p.communicate(input_str))
    print('Output:', output, 'error:', error, 'return:', p.returncode)
    return output, error, p.returncode

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        input_str = request.form['input']
        hex_code = request.form['hexdump']
        output, error, returncode = srs_run(hex_code)
        if returncode:
            return render_template('error.html', code=code, input=input_str, error=error)
        else:
            return render_template('code.html', code=code, input=input_str, output=output)
    else:
        return render_template('primary.html')

@app.route('/link/')
@app.route('/link/<link>')
def link(link='48'):
    url_for('static', filename='logo.ico')
    print('Link:', link)
    ls = link.split('-',1)
    print(ls)
    c = ls[0]
    i = ls[1] if len(ls) > 1 else ''
    print(c, i)
    code = ''
    for x in range(0, len(c), 2):
        code += chr_cp437(int(c[x:x+2],16))
    print('Code:', code)
    if c.upper().startswith('E5'):
        print('http://bit.ly/%s'%(code[1:]))
        return redirect('http://bit.ly/%s'%(code[1:]))
    inputval = u''
    for x in range(0, len(i), 4):
        inputval += unichr(int(i[x:x+4], 16))
    print('Input:', inputval)
    output, error, returncode = srs_run(c)
    if returncode:
        return render_template('error.html', code=code, input=input_str, error=error)
    else:
        return render_template('code.html', code=code, input=input_str, output=output)

if __name__ == '__main__':
    print('Starting server...')
    app.run(host='0.0.0.0',port=80)
