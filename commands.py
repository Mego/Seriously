#!/usr/bin/env python

from __future__ import print_function, division
from fractions import gcd
import operator, cmath
import math as rmath
from types import *

phi = (1+5**.5)/2
Fib = lambda n:int(phi**n/5**.5+.5)

primes = [2,3]

class MathSelector(object):
    def __init__(self, fn):
        self.fn = fn
    def __call__(self,*args):
        try:
            return getattr(rmath,self.fn)(*args)
        except:
            return getattr(cmath,self.fn)(*args)

class Math(object):
    def __getattr__(self, fn):
        if fn in ['pi','e']:
            return getattr(rmath,fn)
        else:
            return MathSelector(fn)
        
math = Math()

def is_prime(x):
    global primes
    if x in primes:
        return 1
    if x<2:
        return 0
    for p in filter(lambda p:p*p<=x,primes):
        if x%p==0:
            return 0
    n = max(primes)+2
    while n*n<=x:
        if x%n==0:
            return 0
    return 1

def init_primes_up_to(n):
    global primes
    if max(primes) > n:
        return
    x = max(primes)+2
    while x < n:
        if is_prime(x):
            primes.append(x)
        x+=2

def nth_prime(n):
    global primes
    while len(primes)<=n:
        init_primes_up_to(max(primes)+100)
    return primes[n]
        
def Fib_index(n):
    a,b=5*n**2+4,5*n**2-4
    if int(a**.5)==a:
        return int(math.log((n*5**.5+a**.5)/2)/math.log(phi))
    elif int(b**.5)==b:
        return int(math.log((n*5**.5+b**.5)/2)/math.log(phi))
    else:
        return -1

def div_fn(srs):
    a=srs.pop()
    if type(a) is ListType:
        srs.push(a[-1:]+a[:-1])
    elif type(a) in [IntType, LongType]:
        b=srs.pop()
        srs.push(a/b)
    else:
        srs.push(a)
        
def idiv_fn(srs):
    a=srs.pop()
    if type(a) is ListType:
        srs.push(a[1:]+a[:1])
    elif type(a) in [IntType,LongType]:
        b=srs.pop()
        srs.push(a//b)
    else:
        srs.push(a)

def dupe_fn(srs):
    a=srs.pop()
    srs.push(a)
    srs.push(a)
    
def rot2_fn(srs):
    a,b=srs.pop(),srs.pop()
    srs.push(a)
    srs.push(b)
    
def deq_fn(srs):
    a=srs.pop()
    if type(a) is ListType:
        b=a.pop(-1)
        srs.push(a)
        srs.push(b)
    else:
        srs.push(a)
        
def i_fn(srs):
    a=srs.pop()
    if type(a) is StringType and (all([c.isdigit() or c=='.' for c in a]) and a.count('.')<2):
        srs.push(float(a))
    elif type(a) is ListType:
        for x in a[::-1]:
            srs.push(x)
    else:
        srs.push(a)
        
def to_list_fn(srs):
    srs.stack = [srs.stack]
    
def psh_fn(srs):
    a=srs.pop()
    b=srs.pop()
    a=[b]+a
    srs.push(a)
    
def p_fn(srs):
    a=srs.pop()
    if type(a) in [IntType, LongType]:
        srs.push(is_prime(a))
    elif type(a) is ListType:
        b=a.pop()
        srs.push(a)
        srs.push(b)
    else:
        srs.push(a)
        
def enq_fn(srs):
    a,b=srs.pop(),srs.pop()
    a.append(b)
    srs.push(a)
    
def flatten(lst):
    return sum(([x] if not isinstance(x, list) else flatten(x) for x in lst), [])
    
def flat_explode_fn(srs):
    tmp = []
    while len(srs.stack)>0:
        a = srs.pop()
        if type(a) is StringType:
            a = a.split('')
        elif type(a) is ListType:
            a = flatten(a)
        tmp.append(a)
    srs.stack = tmp[:]
        
def nrrot_fn(srs):
    a=x.pop()
    srs.stack=srs.stack[a:]+srs.stack[:a]
    
def nlrot_fn(srs):
    a=x.pop()
    srs.stack=srs.stack[:a]+srs.stack[a:]
    
def ins_top_fn(srs):
    a=srs.pop()
    b=srs.pop()
    srs.stack=srs.stack[:a]+[b]+srs.stack[a:]
    
def ins_bot_fn(srs):
    a=srs.pop()
    b=srs.pop()
    srs.stack=srs.stack[:-a]+[b]+srs.stack[-a:]
    
def dupe_all_fn(srs):
    srs.stack=srs.stack[:]+srs.stack[:]
    
def dupe_each_fn(srs):
    tmp=[]
    while len(srs.stack)>0:
        a=srs.pop()
        tmp.append(a)
        tmp.append(a)
    srs.stack=tmp[:]
    
def r_fn(srs):
    a=srs.pop()
    if type(a) is StringType:
        map(srs.push,a.split('')[::-1])
    elif type(a) in [IntType, LongType]:
        srs.push(range(a))
        
def if_fn(srs):
    a,b,c=srs.pop(),srs.pop(),srs.pop()
    srs.push(b if a else c)
    
def invert_fn(srs):
    srs.stack=srs.stack[::-1]
    
def comp_fn(srs):
    a=srs.pop()
    if type(a) is ListType:
        a = a+[0] if a%2 else a
        while len(a) > 0:
            r,i = a.pop(0),a.pop(0)
            srs.push(complex(r,i))
    elif type(a) in [IntType, LongType, FloatType]:
        b=srs.pop()
        srs.push(complex(a,b))
    else:
        srs.push(a)
        
fn_table={32:lambda x:x.push(len(x.stack)),
          33:lambda x:x.push(math.factorial(x.pop())),
          36:lambda x:x.push(str(x.pop())),
          37:lambda x:x.push(x.pop()%x.pop()),
          38:lambda x:x.push(x.pop() & x.pop()),
          40:lambda x:x.push(x.stack.pop(-1)),
          41:lambda x:x.append(x.pop()),
          42:lambda x:x.push(x.pop()*x.pop()),
          43:lambda x:x.push(x.pop()+x.pop()),
          44:lambda x:x.push(input()),
          45:lambda x:x.push(x.pop()-x.pop()),
          46:lambda x:print(x.pop()),
          47:div_fn,
          59:dupe_fn,
          60:lambda x:x.push(int(x.pop()<x.pop())),
          61:lambda x:x.push(int(x.pop()==x.pop())),
          62:lambda x:x.push(int(x.pop()>x.pop())),
          63:lambda x:x,
          64:rot2_fn,
          65:lambda x:x.push(abs(x.pop())),
          67:lambda x:x.push(math.cos(x.pop())),
          68:lambda x:x.push(x.pop()-1),
          69:lambda x:x.push(math.erf(x.pop())),
          70:lambda x:x.push(Fib(x.pop())),
          73:if_fn,
          75:lambda x:x.push(ceil(x.pop())),
          76:lambda x:x.push(floor(x.pop())),
          79:lambda x:map(lambda y:map(x.push,map(ord,y)[::-1]),x.pop()[::-1]),
          80:lambda x:x.push(nth_prime(x.pop())),
          82:lambda x:x.push(range(1,x.pop()+1)),
          83:lambda x:x.push(math.sin(x.pop())),
          84:lambda x:x.push(math.tan(x.pop())),
          85:lambda x:x.push(list(set(x.pop()).union(x.pop()))),
          90:lambda x:x.push(zip(x.pop(),x.pop())),
          92:idiv_fn,
          94:lambda x:x.push(pow(x.pop(),x.pop())),
          95:lambda x:x.push(math.log(x.pop())),
          97:invert_fn,
          98:lambda x:x.push(int(bool(x))),
          99:lambda x:x.push(chr(x.pop()%256)),
          100:deq_fn,
          101:lambda x:x.push(math.exp(x.pop())),
          102:lambda x:x.push(Fib_index(x.pop())),
          103:lambda x:x.push(gcd(x.pop(),x.pop())),
          104:lambda x:x.push(math.hypot(x.pop(),x.pop())),
          105:i_fn,
          106:lambda x:x.push(str.join(x.pop(),map(str,x.pop()))),
          107:to_list_fn,
          108:lambda x:x.push(len(x.pop())),
          109:lambda x:map(x.push,math.modf(x.pop())),
          110:lambda x:map(x.push,(lambda y,z:[y for _ in range(z)])(x.pop(),x.pop())),
          111:psh_fn,
          112:p_fn,
          113:enq_fn,
          114:r_fn,
          115:lambda x:x.push(math.sgn(x.pop())),
          116:flat_explode_fn,
          117:lambda x:x.push(x.pop()+1),
          122:lambda x:map(x.eval,(lambda y:['.' for _ in range(y)])(x.pop())),
          123:nrrot_fn,
          124:lambda x:x.push(x.pop() | x.pop()),
          125:nlrot_fn,
          126:lambda x:x.push(~x.pop()),
          127:lambda x:exit(),
          128:comp_fn,
          129:lambda x:map(print,[x.pop() for _ in len(x.stack)]),
          131:lambda x:x.push(math.asin(x.pop())),
          132:lambda x:x.push(math.acos(x.pop())),
          133:lambda x:x.push(math.atan(x.pop())),
          134:lambda x:x.push(math.atan2(x.pop(),x.pop())),
          135:lambda x:x.push(math.asinh(x.pop())),
          136:lambda x:x.push(math.acosh(x.pop())),
          137:lambda x:x.push(math.atanh(x.pop())),
          139:lambda x:x.push(complex(0,1)),
          140:lambda x:x.push(complex(0,x.pop())),
          142:lambda x:x.push(math.sinh(x.pop())),
          143:lambda x:x.push(math.cosh(x.pop())),
          144:lambda x:x.push(math.tanh(x.pop())),
          155:lambda x:x.push(math.copysign(x.pop(),x.pop())),
          158:lambda x:x.push(cmath.phase(x.pop())),
          160:lambda x:x.push((lambda z:complex(z.real,-z.imag))(x.pop())),
          166:lambda x:x.push(x.pop()**2),
          167:lambda x:x.push(math.degrees(x.pop())),
          169:lambda x:x.push(x.pop()+2),
          170:lambda x:x.push(x.pop()-2),
          171:lambda x:x.push(x.pop()/2),
          172:lambda x:x.push(x.pop()/4),
          174:ins_bot_fn,
          175:ins_top_fn,
          179:dupe_all_fn,
          197:dupe_each_fn,
          203:lambda x:x.push(math.pi),
          204:lambda x:x.push(math.e),
          226:lambda x:x.push(math.gamma(x.pop())),
          227:lambda x:x.push(reduce(operator.mul,x.pop(),1)),
          228:lambda x:x.push(sum(x.pop())),
          237:lambda x:x.push(phi),
          239:lambda x:x.push(set(x.pop()).intersection(x.pop())),
          241:lambda x:x.push(-x.pop()),
          242:lambda x:x.push(x.pop()>=x.pop()),
          243:lambda x:x.push(x.pop()<=x.pop()),
          247:lambda x:x.push(int(x.pop())),
          248:lambda x:x.push(math.radians(x.pop())),
          251:lambda x:x.push(x.pop()**.5),
          }