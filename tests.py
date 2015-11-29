#!/usr/bin/env python
# -*- coding: cp437 -*-

import subprocess

def serious_call(code, input=''):
    p = subprocess.Popen(['./seriously.py','-c',code],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    return p.communicate(input)    
    
def serious_check(code, result, input='', errors=True):
    output, error = serious_call(code, input)
    if errors and error:
        return False
    return output == result
    
# I/O tests
assert serious_check(r'	','a\n','a')
assert serious_check(r',','a\n','"a"')
assert serious_check(r',','12345\n','12345')
assert serious_check(r',','[3, 2, 1]\n','[3,2,1]')

# Literals tests
assert serious_check(r'"a','a\n')
assert serious_check(r"'a",'a\n')
for i in range(10):
    assert serious_check(r'%d'%i,'%d\n'%i)
assert serious_check(r':12345','12345\n')
assert serious_check(r':1.25','1.25\n')
assert serious_check(r':1+2j','(1+2j)\n')
assert serious_check(r'[1,2+0j,"fizz",4.0,"buzz"]',"[1, (2+0j), 'fizz', 4.0, 'buzz']\n")
assert serious_check(r'`foo`','foo\n')
assert serious_check(r'%slen({1,2,2,3})%s'%(chr(0xEC),chr(0xEC)), '3\n')

# Meta stack tests
assert serious_check(r'1 ','1\n1\n')
assert serious_check(r'123(','1\n3\n2\n')
assert serious_check(r'123)','2\n1\n3\n')
assert serious_check(r'123@','2\n3\n1\n')
assert serious_check(r'Q','Q\n')
assert serious_check(r'5W;.D','5\n4\n3\n2\n1\n0\n')
assert serious_check(r'123a','1\n2\n3\n')
assert serious_check(r'123'+chr(0x7F),'')
assert serious_check(r'123'+chr(0xB3),'3\n2\n1\n'*2)
assert serious_check(r'123'+chr(0xC5),'3\n3\n2\n2\n1\n1\n')
assert serious_check(r'12'+chr(0xC6),'1\n1\n')
assert serious_check(r'123'+chr(0xFE),'3 2 1\n3\n2\n1\n')

# Registers tests
assert serious_check(r'1%s2%s%s%s'%(chr(0xBB),chr(0xBC),chr(0xBE),chr(0xBD)),'1\n2\n')
assert serious_check(r'53%s3%s'%(chr(0xBF),chr(0xC0)),'5\n')

# More to come...

