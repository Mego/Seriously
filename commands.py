#!/usr/bin/env python

from __future__ import print_function, division
from fractions import gcd
import operator, cmath
import math as rmath
import random, itertools, sys
from types import *
from base64 import *

phi = (1+5**.5)/2
def Fib(n):
    if n<2:
        return n
    a,b=1,1
    while n>2:
        a,b,n=b,a+b,n-1
    return b

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
        mathmod = cmath if hasattr(cmath,fn) else rmath
        return MathSelector(fn) if callable(getattr(mathmod,fn)) else getattr(rmath,fn)
        
math = Math()

class SeriousFunction(object):
    def __init__(self, code):
        self.code = code
    def __call__(self,srs):
        srs.eval(self.code,print_at_end=False)
    def __str__(self):
        return '%s'%self.code
    def __repr__(self):
        return '`%s`'%self.code
    def __len__(self):
        return len(self.code)
    def __add__(self,other):
        return SeriousFunction(self.code+other.code)
    def __mul__(self,other):
        return SeriousFunction(self.code*other)
    def __mod__(self,other):
        return SeriousFunction(self.code%other)
        
def NinetyNineBottles():
    x = 99
    res = ''
    for i in range(99):
        w = 'Take one down and pass it around, '+str((x-(i+1)))+' bottle{0} of beer on the wall.'.format(['s',''][x-i==2])
        y = str((x-i))+' bottle{0} of beer on the wall, '+str((x-i))+' bottle{0} of beer.'
        y=y.format(['s',''][x-i==1])
        z = 'Go to the store and buy some more, '+str(x)+' bottles of beer on the wall.'
        if i == (x-1):
            res += y + '\n' + z
        else:
            res += y + '\n' + w
        i += 1
        res += '\n\n'
    return res

def is_prime(x):
    global primes
    if x in primes:
        return 1
    if x<2 or (max(primes) > x):
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
        
init_primes_up_to(100)

def nth_prime(n):
    global primes
    while len(primes)<=n:
        init_primes_up_to(max(primes)+100)
    return primes[n]
        
def Fib_index(n):
    i=0
    while Fib(i)<n:
        i+=1
    return i if Fib(i) == n else -1

def div_fn(srs):
    a=srs.pop()
    if type(a) is ListType:
        srs.push(a[-1:]+a[:-1])
    elif type(a) in [IntType, LongType, FloatType, ComplexType]:
        b=srs.pop()
        srs.push(a/b)
    else:
        srs.push(a)
        
def idiv_fn(srs):
    a=srs.pop()
    if type(a) is ListType:
        srs.push(a[1:]+a[:1])
    elif type(a) in [IntType,LongType,FloatType,ComplexType]:
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
        b=a.pop(0)
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
    
def lr_fn(srs):
    a=srs.pop()
    if type(a) is StringType:
        map(srs.push,a[::-1])
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
        
def map_fn(srs):
    f,l=srs.pop(),srs.pop()
    res=[]
    for x in l:
        s = srs.make_new(x)
        f(s)
        res+=s.stack
    srs.push(res)
    
def r_fn(srs):
    a=srs.pop()
    if isinstance(a,SeriousFunction):
        b=srs.pop()
        s=srs.make_new(*b)
        a(s)
        srs.push(s.stack)
    elif type(a) in [StringType,ListType]:
        srs.push(a[::-1])
    else:
        srs.push(range(1,a+1))
        
def n_fn(srs):
    a,b=srs.pop(),srs.pop()
    for i in range(b):
        if isinstance(a, SeriousFunction):
            a(srs)
        else:
            srs.push(a)
            
def full_factor(n):
    global primes
    init_primes_up_to(n)
    res=[]
    for p in filter(lambda x:x<=n,primes):
        a=0
        while n%p==0:
            a+=1
            n//=p
        if a:
            res.append([p,a])
    return res
    
def factor(n):
    return [a for a,b in full_factor(n)]
    
def mod_fn(srs):
    a=srs.pop()
    b=srs.pop()
    if type(a) is StringType or isinstance(a,SeriousFunction):
        srs.push(a%tuple(b))
    else:
        srs.push(a%b)
        
def f_fn(srs):
    a=srs.pop()
    if type(a) is StringType:
        b=srs.pop()
        srs.push(a.format(*b))
    else:
        srs.push(Fib_index(a))
        
def make_list_fn(srs):
    a=srs.pop()
    res=a
    try:
        res=list(a)
    except:
        res=[a]
    srs.push(res)
    
def j_fn(srs):
    a=srs.pop()
    if type(a) in [ListType, StringType]:
        srs.push(random.choice(a))
    else:
        srs.push(random.randrange(a))
        
def star_fn(srs):
    a=srs.pop()
    b=srs.pop()
    if type(a) is ListType:
        srs.push(map(lambda x:x*b,a))
    elif type(b) is ListType:
        srs.push(map(lambda x:x*a,b))
    else:
        srs.push(a*b)
        
def plus_fn(srs):
    a=srs.pop()
    b=srs.pop()
    if type(a) is ListType:
        srs.push(map(lambda x:x+b,a))
    elif type(b) is ListType:
        srs.push(map(lambda x:x+a,b))
    else:
        srs.push(a+b)
        
def digit_to_char(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)

def str_base(number,base):
    if number < 0:
        return '-' + str_base(-number, base)
    (d, m) = divmod(number, base)
    if d > 0:
        return str_base(d, base) + digit_to_char(m)
    return digit_to_char(m)
    
def i_mul_fn(srs):
    a=srs.pop()
    if type(a) is ListType:
        srs.push(map(lambda x:complex(0,x),a))
    else:
        srs.push(complex(0,a))
        
def npop_list_fn(srs):
    a=srs.pop()
    res=[]
    for _ in range(a):
        res.append(srs.pop())
    srs.push(res)
    
def E_fn(srs):
    a=srs.pop()
    if type(a) in [IntType,LongType,FloatType,ComplexType]:
        srs.push(math.erf(a))
    else:
        b=srs.pop()
        srs.push(a[b])
        
def peek_print_fn(srs):
    print(' '.join(map(repr, srs.stack)))
    
def while_fn(srs):
    f=srs.pop()
    while srs.peek():
        f(srs)
        
def dupe_each_n_fn(srs):
    a=srs.pop()
    tmp = []
    while srs.stack:
        b = srs.pop()
        tmp+=[b for i in range(a)]
    srs.stack=tmp[:]
    
def S_fn(srs):
    a=srs.pop()
    if type(a) is StringType:
        srs.push(''.join(sorted(a)))
    elif type(a) is ListType:
        srs.push(sorted(a))
    else:
        srs.push(math.sin(a))
        
def print_all_fn(srs):
    while srs.stack:
        print(srs.pop())
        
def zip_fn(srs):
    a=srs.pop()
    if type(a) in [ListType,StringType]:
        b=srs.pop()
        srs.push(map(list,[filter(lambda x:x is not None,zlist) for zlist in itertools.izip_longest(a,b)]))
    else:
        lists = [srs.pop() for i in range(a)]
        srs.push(map(list,[filter(lambda x:x is not None,zlist) for zlist in itertools.izip_longest(*lists)]))
        
def sum_fn(srs):
    a=srs.pop()
    res = sum(a,type(a[0])()) if type(a[0]) is not StringType else ''.join(map(str,a))
    srs.push(res)
    
def index_fn(srs):
    b,a=srs.pop(),srs.pop()
    if a in b:
        srs.push(b.index(a))
    else:
        srs.push(-1)
        
def cond_quit_fn(srs):
    a=srs.pop() if srs.stack else None
    if a:
        srs.push(a)
    else:
        exit()
        
def median_fn(srs):
    a=srs.pop()
    if len(a)%2:
        srs.push(a[len(a)//2])
    else:
        if all([type(x) is StringType for x in a[len(a)//2-1:][:2]]):
            med = sum(map(ord,a[len(a)//2-1:][:2]))//2
            srs.push(chr(med))
        else:
            srs.push(sum(a[len(a)//2-1:][:2])//2)
            
def c_fn(srs):
    a=srs.pop()
    if type(a) in [ListType,StringType]:
        b=srs.pop()
        srs.push(a.count(b))
    else:
        srs.push(chr(a%256))
        
def exit_fn(srs):
    exit()
        
fn_table={
        0x09:lambda x:x.push(sys.stdin.read(1)),
        0x20:lambda x:x.push(len(x.stack)),
        0x21:lambda x:x.push(math.factorial(x.pop())),
        0x23:make_list_fn,
        0x24:lambda x:x.push(str(x.pop())),
        0x25:mod_fn,
        0x26:lambda x:x.push(x.pop() & x.pop()),
        0x28:lambda x:x.push(x.stack.pop(-1)),
        0x29:lambda x:x.append(x.pop()),
        0x2A:star_fn,
        0x2B:plus_fn,
        0x2C:lambda x:x.push((lambda y:list(y) if type(y) is TupleType else y)(input())),
        0x2D:lambda x:x.push(x.pop()-x.pop()),
        0x2E:lambda x:(lambda y:print(y) if not isinstance(y,SeriousFunction) else y(x) or print(x.pop()))(x.pop()),
        0x2F:div_fn,
        0x3B:dupe_fn,
        0x3C:lambda x:x.push(int(x.pop()<x.pop())),
        0x3D:lambda x:x.push(int(x.pop()==x.pop())),
        0x3E:lambda x:x.push(int(x.pop()>x.pop())),
        0x3F:lambda x:x,
        0x40:rot2_fn,
        0x41:lambda x:x.push(abs(x.pop())),
        0x42:lambda x:x.push(random.randrange(x.pop(),x.pop())),
        0x43:lambda x:x.push(math.cos(x.pop())),
        0x44:lambda x:x.push(x.pop()-1),
        0x45:E_fn,
        0x46:lambda x:x.push(Fib(x.pop())),
        0x47:lambda x:x.push(random.random()),
        0x48:lambda x:x.push("Hello, World!"),
        0x49:if_fn,
        0x4A:j_fn,
        0x4B:lambda x:x.push(math.ceil(x.pop())),
        0x4C:lambda x:x.push(math.floor(x.pop())),
        0x4D:map_fn,
        0x4E:lambda x:x.push(NinetyNineBottles()),
        0x4F:lambda x:map(lambda y:map(x.push,map(ord,y)[::-1]),x.pop()[::-1]),
        0x50:lambda x:x.push(nth_prime(x.pop())),
        0x51:lambda x:x.push(x.code),
        0x52:r_fn,
        0x53:S_fn,
        0x54:lambda x:x.push(math.tan(x.pop())),
        0x55:lambda x:x.push(list(set(x.pop()).union(x.pop()))),
        0x56:lambda x:x.push(random.uniform(x.pop(),x.pop())),
        0x58:lambda x:x.pop(),
        0x59:lambda x:x.push(0 if x.pop() else 1),
        0x5A:zip_fn,
        0x5C:idiv_fn,
        0x5E:lambda x:x.push(pow(x.pop(),x.pop())),
        0x5F:lambda x:x.push(math.log(x.pop())),
        0x61:invert_fn,
        0x62:lambda x:x.push(int(bool(x.pop()))),
        0x63:c_fn,
        0x64:deq_fn,
        0x65:lambda x:x.push(math.exp(x.pop())),
        0x66:lambda x:x.push(Fib_index(x.pop())),
        0x67:lambda x:x.push(gcd(x.pop(),x.pop())),
        0x68:lambda x:x.push(math.hypot(x.pop(),x.pop())),
        0x69:i_fn,
        0x6A:lambda x:x.push(str.join(x.pop(),map(str,x.pop()))),
        0x6B:to_list_fn,
        0x6C:lambda x:x.push(len(x.pop())),
        0x6D:lambda x:map(x.push,math.modf(x.pop())),
        0x6E:n_fn,
        0x6F:psh_fn,
        0x70:p_fn,
        0x71:enq_fn,
        0x72:lr_fn,
        0x73:lambda x:x.push((lambda y:1 if y>0 else -1 if y<0 else 0)(x.pop())),
        0x74:flat_explode_fn,
        0x75:lambda x:x.push(x.pop()+1),
        0x76:lambda x:random.seed(x.pop()),
        0x77:lambda x:x.push(full_factor(x.pop())),
        0x78:lambda x:x.push(range(x.pop(),x.pop())),
        0x79:lambda x:x.push(factor(x.pop())),
        0x7A:lambda x:map(x.eval,(lambda y:['.' for _ in range(y)])(x.pop())),
        0x7B:nrrot_fn,
        0x7C:lambda x:x.push(x.pop() | x.pop()),
        0x7D:nlrot_fn,
        0x7E:lambda x:x.push(~x.pop()),
        0x7F:exit_fn,
        0x80:comp_fn,
        0x81:print_all_fn,
        0x82:lambda x:map(lambda y:x.pop(), range(len(x.stack))),
        0x83:lambda x:x.push(math.asin(x.pop())),
        0x84:lambda x:x.push(math.acos(x.pop())),
        0x85:lambda x:x.push(math.atan(x.pop())),
        0x86:lambda x:x.push(math.atan2(x.pop(),x.pop())),
        0x87:lambda x:x.push(math.asinh(x.pop())),
        0x88:lambda x:x.push(math.acosh(x.pop())),
        0x89:lambda x:x.push(math.atanh(x.pop())),
        0x8A:lambda x:x.push(repr(x.pop())),
        0x8B:lambda x:x.push(complex(0,1)),
        0x8C:i_mul_fn,
        0x8D:lambda x:x.push(1/x.pop()),
        0x8E:lambda x:x.push(math.sinh(x.pop())),
        0x8F:lambda x:x.push(math.cosh(x.pop())),
        0x90:lambda x:x.push(math.tanh(x.pop())),
        0x91:lambda x:x.push((lambda y:sum(y)/len(y) if y else 0)(x.pop())),
        0x92:lambda x:x.push(x.pop().replace(x.pop(),x.pop())),
        0x93:lambda x:x.push(x.pop().strip()),
        0x94:lambda x:x.push(x.pop().lstrip()),
        0x95:lambda x:x.push(x.pop().rstrip()),
        0x96:lambda x:x.push(x.pop().upper()),
        0x97:lambda x:x.push(x.pop().lower()),
        0x98:lambda x:x.push(x.pop().title()),
        0x99:lambda x:x.push(x.pop().swapcase()),
        0x9A:lambda x:x.push((lambda y:max(y,key=y.count))(x.pop())),
        0x9B:lambda x:x.push(math.copysign(x.pop(),x.pop())),
        0x9C:lambda x:x.push(SeriousFunction(x.pop())),
        0x9D:lambda x:x.push(map(operator.add,itertools.izip_longest(x.pop(),x.pop(),fillvalue=0))),
        0x9E:lambda x:x.push(cmath.phase(x.pop())),
        0x9F:lambda x:x.pop()(x),
        0xA0:lambda x:x.push(x.pop().conjugate()),
        0xA1:index_fn,
        0xA2:cond_quit_fn,
        0xA4:lambda x:x.push(map(list,enumerate(x.pop()))),
        0xA6:lambda x:x.push(x.pop()**2),
        0xA7:lambda x:x.push(math.degrees(x.pop())),
        0xA8:lambda x:x.push(int(x.pop(),x.pop())),
        0xA9:lambda x:x.push(x.pop()+2),
        0xAA:lambda x:x.push(x.pop()-2),
        0xAB:lambda x:x.push(x.pop()/2),
        0xAC:lambda x:x.push(x.pop()/4),
        0xAD:lambda x:x.push(str_base(x.pop(),x.pop())),
        0xAE:ins_bot_fn,
        0xAF:ins_top_fn,
        0xB0:lambda x:x.push(list(itertools.compress(x.pop(),x.pop()))),
        0xB1:lambda x:x.push((lambda y:sum([1 if gcd(i,y)==1 else 0 for i in range(1,y+1)]))(x.pop())),
        0xB2:lambda x:x.push(sum([is_prime(i) for i in range(1,x.pop()+1)])),
        0xB3:dupe_all_fn,
        0xB4:lambda x:x.push(1 if gcd(x.pop(),x.pop())==1 else 0),
        0xBA:median_fn,
        0xC5:dupe_each_fn,
        0xC6:dupe_each_n_fn,
        0xC7:npop_list_fn,
        0xCB:lambda x:x.push(math.pi),
        0xCC:lambda x:x.push(math.e),
        0xCE:while_fn,
        0xD1:lambda x:x.push(pow(10,x.pop())),
        0xD2:lambda x:x.push(math.log(x.pop(),10)),
        0xD3:lambda x:x.push(pow(2,x.pop())),
        0xD4:lambda x:x.push(math.log(x.pop(),2)),
        0xD5:lambda x:x.push(math.log(2)),
        0xDD:lambda x:x.push(b64decode(x.pop())),
        0xDE:lambda x:x.push(b64encode(x.pop())),
        0xE2:lambda x:x.push(math.gamma(x.pop())),
        0xE3:lambda x:x.push(reduce(operator.mul,x.pop(),1)),
        0xE4:sum_fn,
        0xE7:lambda x:x.push(x.pop()*2),
        0xED:lambda x:x.push(phi),
        0xEE:lambda x:x.push(""),
        0xEF:lambda x:x.push(list(set(x.pop()).intersection(x.pop()))),
        0xF1:lambda x:x.push(-x.pop()),
        0xF2:lambda x:x.push(x.pop()>=x.pop()),
        0xF3:lambda x:x.push(x.pop()<=x.pop()),
        0xF7:lambda x:x.push(int(x.pop())),
        0xF8:lambda x:x.push(math.radians(x.pop())),
        0xFB:lambda x:x.push(x.pop()**.5),
        0xFE:peek_print_fn,
}