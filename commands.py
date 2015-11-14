#!/usr/bin/env python

from __future__ import print_function, division
from fractions import gcd
import operator, cmath
import math as rmath
import random, itertools
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

class SeriousFunction(object):
    def __init__(self, code):
        self.code = code
    def __call__(self,srs):
        srs.eval(self.code,print_at_end=False)
    def __str__(self):
        return '%s'%self.code
    __repr__ = __str__
    def __len__(self):
        return len(self.code)
        
def NinetyNineBottles():
    x = 99
    res = ''
    for i in range(99):
        w = 'Take one down and pass it around, '+str((x-(i+1)))+' bottle{0} of beer on the wall.'.format(['s',''][x-i==2])
        y = str((x-i))+' bottle{0} of beer on the wall, '+str((x-i))+' bottle{0} of beer'
        y=y.format(['s',''][x-i==1])
        z = 'Go to the Store and buy some more, '+str(x)+' bottles of beer on the wall.'
        if i == (x-1):
            res += y + '\n' + z
        else:
            res += y + '\n' + w
        i += 1
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
    
def lr_fn(srs):
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
        if n%p==0:
            res += [p,n//p]
    return res
    
def factors(n):
    return [a for a,b in full_factor(n)]
    
def mod_fn(srs):
    a=srs.pop()
    b=srs.pop()
    if type(a) is StringType:
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
        
fn_table={32:lambda x:x.push(len(x.stack)),
          33:lambda x:x.push(math.factorial(x.pop())),
          35:make_list_fn,
          36:lambda x:x.push(str(x.pop())),
          37:mod_fn,
          38:lambda x:x.push(x.pop() & x.pop()),
          40:lambda x:x.push(x.stack.pop(-1)),
          41:lambda x:x.append(x.pop()),
          42:star_fn,
          43:plus_fn,
          44:lambda x:x.push(input()),
          45:lambda x:x.push(x.pop()-x.pop()),
          46:lambda x:(lambda y:print(y) if not isinstance(y,SeriousFunction) else y(x) or print(x.pop()))(x.pop()),
          47:div_fn,
          59:dupe_fn,
          60:lambda x:x.push(int(x.pop()<x.pop())),
          61:lambda x:x.push(int(x.pop()==x.pop())),
          62:lambda x:x.push(int(x.pop()>x.pop())),
          63:lambda x:x,
          64:rot2_fn,
          65:lambda x:x.push(abs(x.pop())),
          66:lambda x:x.push(random.randrange(x.pop(),x.pop())),
          67:lambda x:x.push(math.cos(x.pop())),
          68:lambda x:x.push(x.pop()-1),
          69:E_fn,
          70:lambda x:x.push(Fib(x.pop())),
          71:lambda x:x.push(random.random()),
          72:lambda x:x.push("Hello, World!"),
          73:if_fn,
          74:j_fn,
          75:lambda x:x.push(ceil(x.pop())),
          76:lambda x:x.push(floor(x.pop())),
          77:map_fn,
          78:lambda x:x.push(NinetyNineBottles()),
          79:lambda x:map(lambda y:map(x.push,map(ord,y)[::-1]),x.pop()[::-1]),
          80:lambda x:x.push(nth_prime(x.pop())),
          81:lambda x:x.push(x.code),
          82:r_fn,
          83:lambda x:x.push(math.sin(x.pop())),
          84:lambda x:x.push(math.tan(x.pop())),
          85:lambda x:x.push(list(set(x.pop()).union(x.pop()))),
          86:lambda x:x.push(random.uniform(x.pop(),x.pop())),
          88:lambda x:x.pop(),
          89:lambda x:x.push(0 if x.pop() else 1),
          90:lambda x:x.push(map(list,zip(x.pop(),x.pop()))),
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
          110:n_fn,
          111:psh_fn,
          112:p_fn,
          113:enq_fn,
          114:lr_fn,
          115:lambda x:x.push(math.sgn(x.pop())),
          116:flat_explode_fn,
          117:lambda x:x.push(x.pop()+1),
          118:lambda x:random.seed(x.pop()),
          119:lambda x:x.push(full_factor(x.pop())),
          120:lambda x:x.push(range(x.pop(),x.pop())),
          121:lambda x:x.push(factor(x.pop())),
          122:lambda x:map(x.eval,(lambda y:['.' for _ in range(y)])(x.pop())),
          123:nrrot_fn,
          124:lambda x:x.push(x.pop() | x.pop()),
          125:nlrot_fn,
          126:lambda x:x.push(~x.pop()),
          127:lambda x:exit(),
          128:comp_fn,
          129:lambda x:map(print,[x.pop() for _ in len(x.stack)]),
          130:lambda x:map(lambda y:x.pop(), range(len(x.stack))),
          131:lambda x:x.push(math.asin(x.pop())),
          132:lambda x:x.push(math.acos(x.pop())),
          133:lambda x:x.push(math.atan(x.pop())),
          134:lambda x:x.push(math.atan2(x.pop(),x.pop())),
          135:lambda x:x.push(math.asinh(x.pop())),
          136:lambda x:x.push(math.acosh(x.pop())),
          137:lambda x:x.push(math.atanh(x.pop())),
          139:lambda x:x.push(complex(0,1)),
          140:i_mul_fn,
          141:lambda x:x.push(1/x.pop()),
          142:lambda x:x.push(math.sinh(x.pop())),
          143:lambda x:x.push(math.cosh(x.pop())),
          144:lambda x:x.push(math.tanh(x.pop())),
          145:lambda x:x.push((lambda y:sum(y)/len(y) if y else 0)(x.pop())),
          146:lambda x:x.push(x.pop().replace(x.pop(),x.pop())),
          147:lambda x:x.push(x.pop().strip()),
          148:lambda x:x.push(x.pop().lstrip()),
          149:lambda x:x.push(x.pop().rstrip()),
          150:lambda x:x.push(x.pop().upper()),
          151:lambda x:x.push(x.pop().lower()),
          152:lambda x:x.push(x.pop().title()),
          153:lambda x:x.push(x.pop().swapcase()),
          154:lambda x:x.push((lambda y:max(y,key=y.count))(x.pop())),
          155:lambda x:x.push(math.copysign(x.pop(),x.pop())),
          156:lambda x:x.push(SeriousFunction(x.pop())),
          157:lambda x:x.push(map(operator.add,itertools.izip_longest(x.pop(),x.pop(),fillvalue=0))),
          158:lambda x:x.push(cmath.phase(x.pop())),
          159:lambda x:x.pop()(x),
          160:lambda x:x.push(x.pop().conjugate()),
          166:lambda x:x.push(x.pop()**2),
          167:lambda x:x.push(math.degrees(x.pop())),
          168:lambda x:x.push(int(x.pop(),x.pop())),
          169:lambda x:x.push(x.pop()+2),
          170:lambda x:x.push(x.pop()-2),
          171:lambda x:x.push(x.pop()/2),
          172:lambda x:x.push(x.pop()/4),
          173:lambda x:x.push(str_base(x.pop(),x.pop())),
          174:ins_bot_fn,
          175:ins_top_fn,
          176:lambda x:x.push(list(itertools.compress(x.pop(),x.pop()))),
          177:lambda x:x.push((lambda y:sum([1 if gcd(i,y)==1 else 0 for i in range(1,y+1)]))(x.pop())),
          178:lambda x:x.push(sum([is_prime(i) for i in range(1,x.pop()+1)])),
          179:dupe_all_fn,
          180:lambda x:x.push(1 if gcd(x.pop(),x.pop())==1 else 0),
          186:lambda x:x.push((lambda y:y[len(y)//2] if len(y)%2 else sum(y[len(y)//2:len(y)//2+1])/2)(x.pop())),
          197:dupe_each_fn,
          199:npop_list_fn,
          203:lambda x:x.push(math.pi),
          204:lambda x:x.push(math.e),
          209:lambda x:x.push(10**x.pop()),
          226:lambda x:x.push(math.gamma(x.pop())),
          227:lambda x:x.push(reduce(operator.mul,x.pop(),1)),
          228:lambda x:x.push(sum(x.pop())),
          237:lambda x:x.push(phi),
          239:lambda x:x.push(list(set(x.pop()).intersection(x.pop()))),
          241:lambda x:x.push(-x.pop()),
          242:lambda x:x.push(x.pop()>=x.pop()),
          243:lambda x:x.push(x.pop()<=x.pop()),
          247:lambda x:x.push(int(x.pop())),
          248:lambda x:x.push(math.radians(x.pop())),
          251:lambda x:x.push(x.pop()**.5),
          }