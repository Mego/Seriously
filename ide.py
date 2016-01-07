#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from flask import Flask, render_template, url_for, request
from subprocess import Popen, PIPE, check_call
import os, string
from itertools import *

app = Flask(__name__)

cp437table = ''.join(map(chr,range(128))) + u"ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ "

def ord_cp437(c):
    return int(binascii.hexlify(c),16) if int(binascii.hexlify(c),16) in range(256) else -1
    
def chr_cp437(o):
    return cp437table[o]
    
def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)

@app.route('/', methods=['GET', 'POST'])
def index():
    url_for('static', filename='logo.ico')
    if request.method == 'POST':
        code = request.form['code']
        input_str = request.form['input']
        hex_code = request.form['hexdump']
        print('Got code:', hex_code, 'input:', input_str)
        print('Running Seriously code...')
        p = Popen(['./seriously.py', '-q', '-x', '-c', hex_code], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        output, error = map(lambda s: s.decode('utf-8'), p.communicate(input_str))
        print('Output:', output, 'error:', error, 'return:', p.returncode)
        if p.returncode:
            return render_template('error.html', code=code, input=input_str, error=error)
        else:
            return render_template('code.html', code=code, input=input_str, output=output)
    else:
        return render_template('primary.html')

@app.route('/link/')
@app.route('/link/<link>')
def link(link='code=48&input='):
    url_for('static', filename='logo.ico')
    print('Link:', link)
    ls = link.split(';',1)
    c = ls[0]
    i = ls[1] if len(ls) > 1 else ''
    code = ''.join(map(lambda x:chr_cp437(int(''.join(x), 16)), grouper(c, 2)))
    inputval = u''
    for val in grouper(i, 4):
        inputval += unichr(int(val, 16))
    print('Code:', code)
    print('Input:', inputval)
    return render_template('link.html', code=code, inputval=inputval)

if __name__ == '__main__':
    print('Starting server...')
    app.run(host='0.0.0.0',port=8000)
