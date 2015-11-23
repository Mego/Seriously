#!/usr/bin/python

"""Translates a string of hex values to CP437 characters. Characters not in [0-9A-F] are ignored"""

import sys, re
s = sys.stdin.read()
s=re.sub(r"([^0-9A-Fa-f])","",s)
print s
r=''
i=0
while i < len(s):
    r += chr(int(s[i:i+2],16))
    i+=2
print r