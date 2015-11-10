from flask import Flask, render_template, url_for, request
from subprocess import Popen, PIPE, check_call
import os, string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    url_for('static', filename='logo.ico')
    if request.method == 'POST':
        code = request.form['code']
        input = request.form['input']
        print('Got code:', code, 'input:', input)
        print('Running Seriously code...')
        p = Popen(['./seriously.py', '-c', code, '<<<', input], stdout=PIPE, stderr=PIPE)
        output, error = map(lambda s: s.decode('utf-8'), p.communicate())
        print('Output:', output, 'error:', error)
        if p.returncode:
            return render_template('error.html', code=code, input=input, error=error)
        else:
            return render_template('code.html', code=code, input=input, output=output.replace("\n", "\r\n"))
    else:
        return render_template('primary.html')

@app.route('/link/')
@app.route('/link/<link>')
def link(link='code=%22Error+in+linking+code%22o&input='):
    url_for('static', filename='logo.ico')
    print('Link:', link)
    return render_template('link.html', link=link)

if __name__ == '__main__':
    print('Compiling O...')
    check_call(['gcc', 'o.c', '-DIDE', '-o', 'o-ide', '-lm'])
    print('Starting server...')
    app.run(host='0.0.0.0',port=80)
