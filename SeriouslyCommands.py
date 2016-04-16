#!/usr/bin/env python3

try:
    from math import gcd as _gcd
except:
    from fractions import gcd as _gcd
import operator, cmath
import math as rmath
import random, itertools, sys, string, binascii, ast
from base64 import *
from copy import copy
import pyshoco
import collections
from functools import reduce

def memoize(f):
    memo = {}
    def m_fun(*args):
        if args in memo:
            return memo[args]
        else:
            res = f(*args)
            memo[args] = res
            return res
    return m_fun

def template_specialize(fname, *args):
    if fname not in globals():
        def raiseError(*args, **kwargs):
            raise NotImplementedError("This type combination is unimplemented.")

        globals()[fname] = raiseError

    def template_specializer(func):
        old_func = globals()[fname]
        globals()[fname] = lambda *pargs: func(*pargs) if all(isinstance(a, t) for a, t in zip(pargs, args)) else old_func(*pargs)
        return func

    return template_specializer

phi = (1+5**.5)/2

@memoize
def Fib(n):
    if n<2:
        return n
    a,b=1,1
    while n>2:
        a,b,n=b,a+b,n-1
    return b

def prod(iter):
    return reduce(operator.mul, iter, 1)
    
def gcd(*vals):
    if len(vals) == 2:
        return _gcd(*vals)
    else:
        return _gcd(vals[0], gcd(*vals[1:]))

primes = [2,3]

class MathSelector(object):
    def __init__(self, fn):
        self.fn = fn
    def __call__(self, *args, **kwargs):
        try:
            return getattr(rmath,self.fn)(*args, **kwargs)
        except:
            try:
                return getattr(cmath,self.fn)(*args, **kwargs)
            except Exception as e:
                if self.fn == 'factorial':
                    return naive_factorial(*args, **kwargs)
                else:
                    raise e

class Math(object):
    def __getattr__(self, fn):
        mathmod = cmath if hasattr(cmath,fn) else rmath
        return MathSelector(fn) if isinstance(getattr(mathmod,fn), collections.Callable) else getattr(rmath,fn)

math = Math()

def anytype(x, *types):
    return any(isinstance(x,t) for t in types)

class SeriousFunction(object):
    def __init__(self, code):
        if isinstance(code, SeriousFunction):
            self.code = code.code
        elif isinstance(code, str):
            self.code = code
        else:
            raise TypeError

    def __call__(self, srs):
        return srs.eval(self.code)

    def __str__(self):
        return '{}'.format(self.code)

    def __repr__(self):
        return '`{}`'.format(self.code)

    def __len__(self):
        return len(self.code)

    def __add__(self, other):
        return SeriousFunction(self.code+other.code)

    def __mul__(self, other):
        return SeriousFunction(self.code * other)

    def __mod__(self, other):
        return SeriousFunction(self.code % other)

    def __eq__(self, other):
        if not isinstance(other, SeriousFunction):
            if not isinstance(other, str):
                raise TypeError
            else:
                return self.code == other
        else:
            return self.code == other.code


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

def _sum(data, start=None):
    if any(anytype(x, float, complex) for x in data):
        return math.fsum(data)+start
    if start is None:
        return sum(data)
    else:
        return sum(data, start)

def median(data):
    n = len(data)
    if n%2 == 1:
        return data[n//2]
    else:
        i = n//2-1
        return _sum(data[i:i+2])/2

@memoize
def naive_factorial(x):
    res = 1
    while x:
        res *= x
        x -= 1
    return res

@memoize
def nCr(n, k):
    if k > n:
        return 0
    elif k==n:
        return 1
    res = 1
    while k:
        res *= (n+1-k)/k
        k-=1
    return int(res)

@memoize
def nPr(n, k):
    if k > n:
        return 0
    return nCr(n,k)*naive_factorial(k)

def is_prime(x):
    global primes
    if x in primes:
        return 1
    if x<2 or (max(primes) > x):
        return 0
    for p in [p for p in primes if p*p<=x]:
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

@memoize
def Fib_index(n):
    i=0
    while Fib(i)<n:
        i+=1
    return i if Fib(i) == n else -1

def div_fn(srs):
    a=srs.pop()
    if isinstance(a, list):
        srs.push(a[-1:]+a[:-1])
    elif anytype(a, int, float, complex):
        b=srs.pop()
        srs.push(a/b)
    else:
        srs.push(a)

def idiv_fn(srs):
    a=srs.pop()
    if isinstance(a, list):
        srs.push(a[1:]+a[:1])
    elif anytype(a, int, float, complex):
        b=srs.pop()
        srs.push(a//b)
    else:
        srs.push(a)

def dupe_fn(srs):
    a=srs.pop()
    srs.push(a)
    srs.push(copy(a))

def rot2_fn(srs):
    a,b=srs.pop(),srs.pop()
    srs.push(a)
    srs.push(b)

def deq_fn(srs):
    a=srs.pop()
    if isinstance(a, list):
        b=a.pop(-1)
        srs.push(a)
        srs.push(b)
    else:
        srs.push(a)

def i_fn(srs):
    a=srs.pop()
    if isinstance(a, str) and (all([c.isdigit() or c=='.' for c in a]) and a.count('.')<2):
        srs.push(float(a))
    elif isinstance(a, list):
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
    if isinstance(a, int):
        srs.push(is_prime(a))
    elif isinstance(a, list):
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
        if isinstance(a, str):
            a = a.split('')
        elif isinstance(a, list):
            a = flatten(a)
        tmp.append(a)
    srs.stack = tmp[:]

def nrrot_fn(srs):
    a=srs.pop()
    srs.stack=srs.stack[a:]+srs.stack[:a]

def nlrot_fn(srs):
    a=-srs.pop()
    srs.stack=srs.stack[a:]+srs.stack[:a]

def ins_top_fn(srs):
    a=srs.pop()
    b=srs.pop()
    srs.stack=srs.stack[:a]+[b]+srs.stack[a:]

def ins_bot_fn(srs):
    a=srs.pop()
    b=srs.pop()
    srs.stack=srs.stack[:-a]+[b]+srs.stack[-a:]

def dupe_all_fn(srs):
    srs.stack=[copy(x) for x in srs.stack[:]]+srs.stack[:]

def dupe_each_fn(srs):
    tmp=[]
    while len(srs.stack)>0:
        a=srs.pop()
        tmp.append(a)
        tmp.append(copy(a))
    srs.stack=tmp[::-1]

def lr_fn(srs):
    a=srs.pop()
    if isinstance(a, str):
        list(map(srs.push,a[::-1]))
    elif isinstance(a, int):
        srs.push(list(range(a)))

def s_fn(srs):
    a=srs.pop()
    if isinstance(a, str):
        b=srs.pop()
        if isinstance(b, list):
            try:
                b=''.join(b)
            except TypeError:
                b=''.join(map(repr,b))
        if not anytype(b, list, str):
            b=repr(b)
        srs.push([''.join(list(g)) for k,g in itertools.groupby(a,lambda x:x in b) if not k])
    elif isinstance(a, list):
        b=srs.pop()
        if not anytype(b, list, str):
            b=[b]
        srs.push([list(g) for k,g in itertools.groupby(a,lambda x:x in b) if not k])
    else:
        srs.push(1 if a>0 else -1 if a<0 else 0)

def if_fn(srs):
    a,b,c=srs.pop(),srs.pop(),srs.pop()
    srs.push(b if a else c)

def invert_fn(srs):
    srs.stack=srs.stack[::-1]

def comp_fn(srs):
    a=srs.pop()
    if isinstance(a, list):
        a = a+[0] if len(a)%2 else a
        while len(a) > 0:
            r,i = a.pop(0),a.pop(0)
            srs.push(complex(r,i))
    elif anytype(a, int, float):
        b=srs.pop()
        srs.push(complex(a,b))
    else:
        srs.push(a)

def M_fn(srs):
    a=srs.pop()
    if anytype(a, str, list):
        srs.push(max(a))
    else:
        b=srs.pop()
        if srs.debug_mode:
            print('mapping {} over {}'.format(a, b))
        res=[]
        for x in b:
            s = srs.make_new(x)
            r = a(s)
            res.extend(r)
        srs.push(res)

def r_fn(srs):
    a=srs.pop()
    if isinstance(a,SeriousFunction):
        b=srs.pop()
        s=srs.make_new(*b)
        a(s)
        srs.push(s.stack)
    elif anytype(a, str, list):
        srs.push(a[::-1])
    else:
        srs.push(list(range(1,a+1)))

def n_fn(srs):
    a,b=srs.pop(),srs.pop()
    for i in range(b):
        if isinstance(a, SeriousFunction):
            a(srs)
        else:
            srs.push(a)

@memoize
def full_factor(n):
    n=abs(n)
    global primes
    init_primes_up_to(n)
    res=[]
    for p in [x for x in primes if x<=n]:
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
    if anytype(a, str, SeriousFunction):
        srs.push(a%tuple(b))
    else:
        srs.push(a%b)

def f_fn(srs):
    a=srs.pop()
    if isinstance(a, str):
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
    if anytype(a, list, str):
        srs.push(random.choice(a))
    else:
        srs.push(random.randrange(a))

def star_fn(srs):
    a=srs.pop()
    b=srs.pop()
    if isinstance(a, list) and not isinstance(b, list):
        srs.push([x*b for x in a])
    elif isinstance(b, list) and not isinstance(a, list):
        srs.push([x*a for x in b])
    elif isinstance(a, list) and isinstance(b, list):
        if(len(b) > len(a)):
            a,b=b,a
        while len(b) < len(a):
            b.append(0)
        srs.push(_sum([prod(x) for x in zip(a,b)]))
    else:
        srs.push(a*b)

def plus_fn(srs):
    a=srs.pop()
    b=srs.pop()
    if isinstance(a, list) ^ isinstance(b, list):
        if isinstance(a, list):
            srs.push([x+b for x in a])
        elif isinstance(b, list):
            srs.push([x+a for x in b])
    else:
        srs.push(a+b)

def digit_to_char(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)

def str_base(number,base):
    if number < 0:
        return '-' + str_base(-number, base)
    if isinstance(number, float): return str_base_float(number,base,0)
    (d, m) = divmod(number, base)
    if d > 0:
        return str_base(d, base) + digit_to_char(m)
    return digit_to_char(m)

def str_base_float(number,base,exp):
    if number >= base:
        return str_base_float(number/base,base,exp+1)
    if exp<-15 or (number == 0 and exp < 0):            #15 places after the dot should be good, right?
        return ""
    return digit_to_char(int(number)) + ("." if exp==0 and number%1 else "") + str_base_float((number%1)*base,base,exp-1)

def i_mul_fn(srs):
    a=srs.pop()
    if isinstance(a, list):
        srs.push([complex(0,x) for x in a])
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
    if anytype(a, int, float, complex):
        srs.push(math.erf(a))
    else:
        b=srs.pop()
        srs.push(a[b])

def peek_print_fn(srs):
    print(' '.join(map(repr, srs.stack[::-1])))

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
    srs.stack=tmp[::-1]

def S_fn(srs):
    a=srs.pop()
    if isinstance(a, str):
        srs.push(''.join(sorted(a)))
    elif isinstance(a, list):
        srs.push(sorted(a))
    else:
        srs.push(math.sin(a))

def print_all_fn(srs):
    while srs.stack:
        print(srs.pop())

def zip_fn(srs):
    a=srs.pop()
    if anytype(a, str, list):
        b=srs.pop()
        srs.push(list(map(list,[[x for x in zlist if x is not None] for zlist in itertools.zip_longest(a,b)])))
    else:
        lists = [srs.pop() for i in range(a)]
        srs.push(list(map(list,[[x for x in zlist if x is not None] for zlist in itertools.zip_longest(*lists)])))

def sum_fn(srs):
    a=srs.pop()
    res = _sum(a,start=type(a[0])()) if not isinstance(a[0], str) else ''.join(map(str,a))
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
        if all([isinstance(x, str) for x in a[len(a)//2-1:][:2]]):
            med = median(list(map(ord,a)))
            srs.push(chr(med))
        else:
            srs.push(median(a))

def c_fn(srs):
    a=srs.pop()
    if anytype(a, list, str):
        b=srs.pop()
        srs.push(a.count(b))
    else:
        srs.push(chr(a%256))

def exit_fn(srs):
    exit()

registers = dict()

def get_reg(i):
    global registers
    return registers[i]

def set_reg(i, val):
    global registers
    registers[i] = val

def diff_fn(srs):
    a,b=srs.pop(),srs.pop()
    if all([anytype(x, str, list) for x in (a,b)]):
        srs.push([x for x in a if x not in b])
    else:
        srs.push(a-b)

def m_fn(srs):
    a=srs.pop()
    if anytype(a, str, list):
        srs.push(min(a))
    else:
        srs.push(list(math.modf(a)))

def filter_types(iter,*types):
    return [x for x in iter if anytype(x, types)]

def inv_fil_fn(srs):
    a=srs.pop()
    if isinstance(a, list):
        srs.push(filter_types(a, int, float, complex))
    else:
        srs.push(1/a)

def AE_fn(srs):
    a=srs.pop()
    if isinstance(a, list):
        srs.push(filter_types(a, str))
    else:
        b,c=srs.pop(),srs.pop()
        srs.push(a.replace(b,c))

def fn_fil_fn(srs):
    a=srs.pop()
    if isinstance(a, list):
        srs.push([x for x in a if isinstance(x, SeriousFunction)])
    else:
        srs.push(SeriousFunction(a))

def get_input_fn(srs):
    a=input()
    b = ast.literal_eval(a)
    b = list(b) if isinstance(b, tuple) else b
    srs.push(b)

def T_fn(srs):
    a=srs.pop()
    if anytype(a, int, float, complex):
        srs.push(math.tan(a))
    else:
        b,c = srs.pop(), srs.pop()
        if isinstance(a, str):
            a = a[:b] + str(c) + a[b+1:]
        else:
            a[b] = c
        srs.push(a)

def O_fn(srs):
    a = srs.pop()
    if isinstance(a, list):
        a = ''.join(flatten(a))
    srs.push(list(map(ord,a)))

def dig_fn(srs):
    a = srs.pop()
    l = len(srs.stack)
    a = a % l
    srs.stack = [srs.stack[a]]+srs.stack[:a]+srs.stack[a+1:]

def D_fn(srs):
    a = srs.pop()
    if isinstance(a, list):
        E = sum(a)/len(a)
        srs.push((sum([(E-X)**2 for X in a])/len(a))**.5)
    else:
        srs.push(a-1)

def reg_all_input_fn(srs):
    global registers
    for i,n in enumerate(sys.stdin.read().split('\n')):
        a = ast.literal_eval(n)
        a = list(a) if isinstance(a, tuple) else a
        registers[i] = a


def range_ab_fn(srs):
    a = srs.pop()
    if isinstance(a, list):
        srs.push(list(range(*a)))
    else:
        b = srs.pop()
        srs.push(list(range(a,b)))

def cart_prod_fn(srs):
    #lambda x:x.push(map(list,itertools.product(x.pop(),x.pop())))
    a,b = srs.pop(),srs.pop()
    if anytype(b, int, float):
        srs.push(list(map(list,itertools.product(a,repeat=b))))
    else:
        srs.push(list(map(list,itertools.product(a,b))))

def print_fn(srs):
    a = srs.pop()
    if isinstance(a, SeriousFunction):
        a(srs)
    else:
        print(a)

def nprint_fn(srs):
    n = srs.pop()
    for i in range(n):
        print_fn(srs)
        
def N_fn(srs):
    if len(srs.stack) == 0:
        srs.push(NinetyNineBottles())
    else:
        a,b = srs.pop(), srs.pop()
        srs.push(b[:a] if a>=0 else b[a:])
        
def shuffle_fn(srs):
    a = srs.pop()
    random.shuffle(a)
    srs.push(a)
    
def g_fn(srs):
    a = srs.pop()
    if isinstance(a, list):
        srs.push(gcd(*a))
    else:
        b = srs.pop()
        srs.push(gcd(a,b))
        
def reduce_fn(srs):
    a = srs.pop()
    if isinstance(a, list):
        srs.push([x//gcd(*a) for x in a])
    else:
        b = srs.pop()
        srs.push(b//gcd(a,b))
        srs.push(a//gcd(a,b))

fn_table={
        0x09:lambda x:x.push(sys.stdin.read(1)),
        0x0C:lambda x:x.push(sys.stdin.read()),
        0x1F:reduce_fn,
        0x20:lambda x:x.push(len(x.stack)),
        0x21:lambda x:x.push(math.factorial(x.pop())),
        0x23:make_list_fn,
        0x24:lambda x:x.push(str(x.pop())),
        0x25:mod_fn,
        0x26:lambda x:x.push(x.pop() & x.pop()),
        0x28:lambda x:x.push(x.stack.pop(0)),
        0x29:lambda x:x.prepend(x.pop()),
        0x2A:star_fn,
        0x2B:plus_fn,
        0x2C:get_input_fn,
        0x2D:diff_fn,
        0x2E:print_fn,
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
        0x44:D_fn,
        0x45:E_fn,
        0x46:lambda x:x.push(Fib(x.pop())),
        0x47:lambda x:x.push(random.random()),
        0x48:lambda x:x.push("Hello, World!"),
        0x49:if_fn,
        0x4A:j_fn,
        0x4B:lambda x:x.push(math.ceil(x.pop())),
        0x4C:lambda x:x.push(math.floor(x.pop())),
        0x4D:M_fn,
        0x4E:N_fn,
        0x4F:O_fn,
        0x50:lambda x:x.push(nth_prime(x.pop())),
        0x51:lambda x:x.push(x.code),
        0x52:r_fn,
        0x53:S_fn,
        0x54:T_fn,
        0x55:lambda x:x.push(list(set(x.pop()).union(x.pop()))),
        0x56:lambda x:x.push(random.uniform(x.pop(),x.pop())),
        0x58:lambda x:x.pop(),
        0x59:lambda x:x.push(0 if x.pop() else 1),
        0x5A:zip_fn,
        0x5C:idiv_fn,
        0x5E:lambda x:x.push(x.pop() ^ x.pop()),
        0x5F:lambda x:x.push(math.log(x.pop())),
        0x61:invert_fn,
        0x62:lambda x:x.push(int(bool(x.pop()))),
        0x63:c_fn,
        0x64:deq_fn,
        0x65:lambda x:x.push(math.exp(x.pop())),
        0x66:f_fn,
        0x67:g_fn,
        0x68:lambda x:x.push(math.hypot(x.pop(),x.pop())),
        0x69:i_fn,
        0x6A:lambda x:x.push(str.join(x.pop(),list(map(str,x.pop())))),
        0x6B:to_list_fn,
        0x6C:lambda x:x.push(len(x.pop())),
        0x6D:m_fn,
        0x6E:n_fn,
        0x6F:psh_fn,
        0x70:p_fn,
        0x71:enq_fn,
        0x72:lr_fn,
        0x73:s_fn,
        0x74:flat_explode_fn,
        0x75:lambda x:x.push(x.pop()+1),
        0x76:lambda x:random.seed(x.pop()),
        0x77:lambda x:x.push(full_factor(x.pop())),
        0x78:range_ab_fn,
        0x79:lambda x:x.push(factor(x.pop())),
        0x7A:nprint_fn,
        0x7B:nrrot_fn,
        0x7C:lambda x:x.push(x.pop() | x.pop()),
        0x7D:nlrot_fn,
        0x7E:lambda x:x.push(~x.pop()),
        0x7F:exit_fn,
        0x80:comp_fn,
        0x81:print_all_fn,
        0x82:lambda x:[x.pop() for y in range(len(x.stack))],
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
        0x8D:inv_fil_fn,
        0x8E:lambda x:x.push(math.sinh(x.pop())),
        0x8F:lambda x:x.push(math.cosh(x.pop())),
        0x90:lambda x:x.push(math.tanh(x.pop())),
        0x91:lambda x:x.push((lambda y:mean(y) if y else 0)(x.pop())),
        0x92:AE_fn,
        0x93:lambda x:x.push(x.pop().strip()),
        0x94:lambda x:x.push(x.pop().lstrip()),
        0x95:lambda x:x.push(x.pop().rstrip()),
        0x96:lambda x:x.push(x.pop().upper()),
        0x97:lambda x:x.push(x.pop().lower()),
        0x98:lambda x:x.push(x.pop().title()),
        0x99:lambda x:x.push(x.pop().swapcase()),
        0x9A:lambda x:x.push((lambda y:max(y,key=y.count))(x.pop())),
        0x9B:lambda x:x.push(math.copysign(x.pop(),x.pop())),
        0x9C:fn_fil_fn,
        0x9D:lambda x:x.push(list(map(operator.add,itertools.zip_longest(x.pop(),x.pop(),fillvalue=0)))),
        0x9E:lambda x:x.push(cmath.phase(x.pop())),
        0x9F:lambda x:SeriouslyFunction(x.pop())(x),
        0xA0:lambda x:x.push(x.pop().conjugate()),
        0xA1:index_fn,
        0xA2:cond_quit_fn,
        0xA3:lambda x:x.push(''.join(map(chr,list(range(97,122+1))))),
        0xA4:lambda x:x.push(list(map(list,enumerate(x.pop())))),
        0xA5:lambda x:x.push(filter_types(x.pop(), list)),
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
        0xB9:lambda x:x.push((lambda y:[nCr(y,k) for k in range(y+1)])(x.pop())),
        0xBA:median_fn,
        0xBB:lambda x:set_reg(0,x.pop()),
        0xBC:lambda x:set_reg(1,x.pop()),
        0xBD:lambda x:x.push(get_reg(0)),
        0xBE:lambda x:x.push(get_reg(1)),
        0xBF:lambda x:set_reg(x.pop(),x.pop()),
        0xC0:lambda x:x.push(get_reg(x.pop())),
        0xC2:lambda x:x.push(list(map(list, list(zip(*x.pop()))))),
        0xC5:dupe_each_fn,
        0xC6:dupe_each_n_fn,
        0xC7:npop_list_fn,
        0xC8:shuffle_fn,
        0xCA:reg_all_input_fn,
        0xCB:lambda x:x.push(math.pi),
        0xCC:lambda x:x.push(math.e),
        0xCE:while_fn,
        0xCF:lambda x:x.push(list(map(list,itertools.combinations(x.pop(),x.pop())))),
        0xD0:lambda x:x.push(list(map(list,itertools.permutations(x.pop(),x.pop())))),
        0xD1:lambda x:x.push(pow(10,x.pop())),
        0xD2:lambda x:x.push(math.log(x.pop(),10)),
        0xD3:lambda x:x.push(pow(2,x.pop())),
        0xD4:lambda x:x.push(math.log(x.pop(),2)),
        0xD5:lambda x:x.push(math.log(2)),
        0xDB:lambda x:x.push(nCr(x.pop(),x.pop())),
        0xDC:lambda x:x.push(nPr(x.pop(),x.pop())),
        0xDD:lambda x:x.push(b64decode(x.pop())),
        0xDE:lambda x:x.push(b64encode(x.pop())),
        0xDF:lambda x:x.push(("0123456789"+string.ascii_uppercase+string.ascii_lowercase+"+/")[:x.pop()]),
        0xE2:lambda x:x.push(math.gamma(x.pop())),
        0xE3:lambda x:x.push(reduce(operator.mul,x.pop(),1)),
        0xE4:sum_fn,
        0xE7:lambda x:x.push(x.pop()*2),
        0xEB:dig_fn,
        0xEC:lambda x:x.toggle_preserve(),
        0xED:lambda x:x.push(phi),
        0xEE:lambda x:x.push(""),
        0xEF:lambda x:x.push(list(set(x.pop()).intersection(x.pop()))),
        0xF0:lambda x:x.push(eval(x.pop())),
        0xF1:lambda x:x.push(-x.pop()),
        0xF2:lambda x:x.push(x.pop()>=x.pop()),
        0xF3:lambda x:x.push(x.pop()<=x.pop()),
        0xF4:lambda x:x.push(pyshoco.compress(x.pop())),
        0xF5:lambda x:x.push(pyshoco.decompress(x.pop())),
        0xF7:lambda x:x.push(int(x.pop())),
        0xF8:lambda x:x.push(math.radians(x.pop())),
        0xF9:cart_prod_fn,
        0xFB:lambda x:x.push(x.pop()**.5),
        0xFC:lambda x:x.push(pow(x.pop(),x.pop())),
        0xFD:lambda x:x.push(x.pop()**2),
        0xFE:peek_print_fn,
}
