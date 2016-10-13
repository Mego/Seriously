#!/usr/bin/env python3

import operator, cmath
import math as rmath
import random, itertools, sys, string, binascii, ast
from base64 import *
from copy import copy
import collections
from functools import reduce, lru_cache
import struct
from itertools import zip_longest as izip
from lib.cp437 import CP437
from lib.iterable import deque, as_list, zip_longest

try:
    from statistics import mean, median, mode, pstdev
except ImportError:
    from stats import mean, median, mode, pstdev

from lib.cp437 import CP437

chr_cp437 = CP437.chr
ord_cp437 = CP437.ord

memoize = lru_cache(maxsize=None)

##this will eventually get used hopefully
# def template_specialize(fname, *args):
    # if fname not in globals():
        # def raiseError(*args, **kwargs):
            # raise NotImplementedError("This type combination is unimplemented.")

        # globals()[fname] = raiseError

    # def template_specializer(func):
        # old_func = globals()[fname]
        # globals()[fname] = lambda *pargs: func(*pargs) if all(isinstance(a, t) for a, t in zip(pargs, args)) else old_func(*pargs)
        # return func

    # return template_specializer

phi = (1+5**.5)/2

@memoize
def Lucas(n): # pragma: no cover
    [a,b] = fast_fib(n)
    return (a<<1)+b

fib_cache = {0:0, 1:1, 2:1}

def Fib(n):
    global fib_cache
    if n in fib_cache:
        return fib_cache[n]
    else:
        result = fast_fib(n)[1]
        fib_cache[n] = result
        return result

# F(2n) = (F(n-1) + F(n+1)) * F(n)
#       = (F(n-1) + F(n-1) + F(n)) * F(n)
#       = (2F(n-1) + F(n)) * F(n)

# F(2n-1) = F(n-1)*F(n-1) + F(n)*F(n)

# this returns [F(n-1), F(n)], so
# the implementation should be
# fast_fib(1000)[1]
def fast_fib(n):
    global fib_cache
    if n==0: return [1,0]
    shift = n>>1
    if shift in fib_cache and shift-1 in fib_cache:
        [a,b] = [fib_cache[shift-1],fib_cache[shift]]
    else:
        [a,b] = fast_fib(shift)
        fib_cache[shift-1] = a
        fib_cache[shift] = b
    b2 = b*b
    a,b = a*a+b2, (a<<1)*b+b2
    if n%2 == 1:
        fib_cache[n-1] = b
        return [b,a+b]
    fib_cache[n-1] = a
    return [a,b]

def prod(iter):
    return reduce(operator.mul, iter, 1)

@memoize
def gcd(a,b):
    return b if a==0 else gcd(b%a,a)

@memoize
def gcd_list(*vals):
    return reduce(gcd,vals or [1])

class MathSelector(object):
    def __init__(self, fn):
        self.fn = fn
    def __call__(self, *args, **kwargs):
        try:
            return getattr(rmath,self.fn)(*args, **kwargs)
        except:
            return getattr(cmath,self.fn)(*args, **kwargs)

class Math(object):
    def __getattr__(self, fn):
        mathmod = cmath if hasattr(cmath,fn) else rmath
        return MathSelector(fn) if isinstance(getattr(mathmod,fn), collections.Callable) else getattr(rmath,fn)

math = Math()

def anytype(x, *types):
    return any(isinstance(x,t) for t in types) if types else False

def filter_types(iter,*types,exclude=None):
    if exclude is not None:
        return [x for x in iter if anytype(x, *types) and not anytype(x, *exclude)]
    else:
        return [x for x in iter if anytype(x, *types)]

class SeriousFunction:
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

    __radd__ = __add__

    def __mul__(self, other):
        return SeriousFunction(self.code * other)

    __rmul__ = __mul__

    def __mod__(self, other):
        return SeriousFunction(self.code % other)

    __rmod__ = __mod__

    def __eq__(self, other):
        if not isinstance(other, SeriousFunction):
            if not isinstance(other, str):
                raise NotImplemented
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

@memoize
def nCr(n, k):
    if k > n:
        return 0
    elif k == n:
        return 1
    return math.factorial(n)//(math.factorial(k)*math.factorial(n-k))

@memoize
def nPr(n, k):
    if k > n:
        return 0
    elif k == n:
        return 1
    return math.factorial(n)//math.factorial(n-k)

primes = [2,3]
max_tested = 4

def is_prime(x):
    global primes
    if x in primes:
        return 1
    if x<2 or (primes[-1] > x):
        return 0
    for p in primes:
        if x%p==0:
            return 0
        if p*p>x:
            break
    for test in range(primes[-1]+2,int(rmath.sqrt(x))+1):
        if x%test==0:
            return 0
    return 1

def init_n_primes(n):
    global primes, max_tested
    while len(primes)<=n:
        temp=[1]*max_tested
        for p in primes:
            for q in range((p-max_tested)%p,max_tested,p):
                temp[q] = 0
        primes += [x+max_tested for x in range(max_tested) if temp[x]]
        max_tested *= 2

def init_primes_up_to(n):
    global primes, max_tested
    if max_tested<n:
        temp=[1]*(n-max_tested)
        max_tested += 1
        for p in primes:
            for q in range((p-max_tested)%p,n-max_tested,p):
                temp[q] = 0
        for p in range(n//2-max_tested):
            if temp[p]:
                for q in range(p+p+max_tested,n-max_tested,p+max_tested):
                    temp[q] = 0
        primes += [x+max_tested for x in range(n-max_tested+1) if temp[x]]
        max_tested = n

def nth_prime(n):
    global primes
    init_n_primes(n)
    return primes[n]

def prime_count_fn(srs):
    a=srs.pop()
    if isinstance(a,int):
        global primes, max_tested
        init_primes_up_to(a)
        if max_tested >= a:
            srs.push(len(primes))
        else:
        #binary search
            lo=0
            hi=len(primes)-1
            while lo<hi-1:
                test = (lo+hi)//2
                if primes[test]<=1:
                    lo=test
                else:
                    hi=test
            srs.push(lo+1)
    else:
        srs.push(a)

@memoize
def Fib_index(n):
    i=0
    while Fib(i)<n:
        i+=1
    return i if Fib(i) == n else -1

def div_fn(srs):
    a=srs.pop()
    if isinstance(a, collections.Iterable):
        a = [x for x in a]
        srs.push(a[-1:]+a[:-1])
    elif anytype(a, int, float, complex):
        b=srs.pop()
        srs.push(a/b)
    else:
        srs.push(a)

def idiv_fn(srs):
    a=srs.pop()
    if isinstance(a, collections.Iterable):
        a = [x for x in a]
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

def d_fn(srs):
    a=srs.pop()
    if isinstance(a, collections.Iterable) and not isinstance(a, str):
        a=[x for x in a]
        b=a.pop(-1)
        srs.push(a)
        srs.push(b)
    elif isinstance(a, str):
        b = a[-1]
        srs.push(''.join(a[:-1]))
        srs.push(b)
    else:
        b = srs.pop()
        srs.push(a%b)
        srs.push(a//b)

def i_fn(srs):
    a=srs.pop()
    if isinstance(a, str) and (all([c.isdigit() or c=='.' for c in a]) and a.count('.')<2):
        srs.push(float(a))
    elif isinstance(a, collections.Iterable):
        for x in [y for y in a][::-1]:
            srs.push(x)
    else:
        srs.push(a)

def to_list_fn(srs):
    srs.stack = deque([as_list(srs.stack)])

def psh_fn(srs):
    a=srs.pop()
    b=srs.pop()
    if isinstance(a, str):
        a = b+a
    else:
        a = [b]+a
    srs.push(a)

def p_fn(srs):
    a=srs.pop()
    if isinstance(a, int):
        srs.push(is_prime(a))
    elif isinstance(a, collections.Iterable) and not isinstance(a, str):
        a=[x for x in a]
        b=a.pop(0)
        srs.push(a)
        srs.push(b)
    elif isinstance(a, str):
        b = a[0]
        srs.push(a[1:])
        srs.push(b)
    else:
        srs.push(a)

def enq_fn(srs):
    a,b=srs.pop(),srs.pop()
    if isinstance(a, str):
        a += b
    else:
        a.append(b)
    srs.push(a)

def flatten(lst):
    return sum(([x] if not isinstance(x, collections.Iterable) or isinstance(x, str) else flatten(x) for x in lst), [])

def nrrot_fn(srs):
    a = srs.pop()
    srs.stack.rotate(-a)

def nlrot_fn(srs):
    a = srs.pop()
    srs.stack.rotate(a)

def ins_top_fn(srs):
    a=srs.pop()
    b=srs.pop()
    srs.stack=deque(srs.stack[:a]+[b]+srs.stack[a:])

def ins_bot_fn(srs):
    a=srs.pop()
    b=srs.pop()
    srs.stack=deque(srs.stack[:-a]+[b]+srs.stack[-a:])

def dupe_all_fn(srs):
    srs.stack.extend(copy(x) for x in srs.stack.copy())

def dupe_each_fn(srs):
    tmp=[]
    while len(srs.stack)>0:
        a=srs.pop()
        tmp.append(a)
        tmp.append(copy(a))
    srs.stack=deque(tmp[::-1])

def lr_fn(srs):
    a=srs.pop()
    srs.push(range(a))

def s_fn(srs):
    a=srs.pop()
    if isinstance(a, str):
        b=srs.pop()
        if isinstance(b, collections.Iterable):
            try:
                b=''.join(b)
            except TypeError:
                b=''.join(map(repr,b))
        if not anytype(b, collections.Iterable):
            b=repr(b)
        res = [''.join(list(g)) for k,g in itertools.groupby(a,lambda x:x in b) if not k]
        if a.startswith(b):
            res = ['']+res
        if a.endswith(b):
            res = res+['']
        srs.push(res)
    elif isinstance(a, collections.Iterable):
        b=srs.pop()
        if not anytype(b, collections.Iterable):
            b=[b]
        res = [list(g) for k,g in itertools.groupby(a,lambda x:x in b) if not k]
        splitter = b
        if isinstance(splitter, str):
            splitter = list(splitter)
        if a[:len(b)] == splitter:
            res = res+[[]]
        if a[-len(b):] == splitter:
            res = [[]]+res
        srs.push(res)
    else:
        srs.push(1 if a>0 else -1 if a<0 else 0)

def if_fn(srs):
    a,b,c=srs.pop(),srs.pop(),srs.pop()
    srs.push(b if a else c)

def invert_fn(srs):
    srs.stack=srs.stack.reversed()

def comp_fn(srs):
    a=srs.pop()
    if isinstance(a, collections.Iterable):
        a = [x for x in a]
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
    if anytype(a, collections.Iterable):
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

def R_fn(srs):
    a=srs.pop()
    if isinstance(a,SeriousFunction):
        b=srs.pop()
        s=srs.make_new(*b)
        a(s)
        srs.push(s.stack)
    elif anytype(a, collections.Iterable):
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

@memoize
def full_factor(n):
    global primes
    n=abs(n)
    res=[]
    index = 0
    init_primes_up_to(int(rmath.sqrt(n)))
    for p in primes:
        a=0
        while n%p==0:
            a+=1
            n//=p
        if a:
            res.append([p,a])
        if n==1:
            break
    if n>1:
        # n is a prime at this point, but please don't add
        # it to the prime list as it would mess up the prime
        # list since the prime list would not be continuous
        res.append([n,1])
    return res

def factor(n):
    return [a for a,b in full_factor(n)]

def mod_fn(srs):
    a=srs.pop()
    b=srs.pop()
    if anytype(a, str, SeriousFunction):
        srs.push(a%(tuple(b) if not isinstance(b, str) else (b,)))
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
    if anytype(a, collections.Iterable):
        srs.push(random.choice(a))
    else:
        srs.push(random.randrange(a))

def star_fn(srs):
    a=srs.pop()
    b=srs.pop()
    if (isinstance(a, str) and not isinstance(b, collections.Iterable)) or (isinstance(b, str) and not isinstance(a, collections.Iterable)):
        srs.push(a*b)
    elif isinstance(a, collections.Iterable) and (not isinstance(b, collections.Iterable) or isinstance(b, str)):
        srs.push([x*b for x in a])
    elif isinstance(b, collections.Iterable) and (not isinstance(a, collections.Iterable) or isinstance(a, str)):
        srs.push([x*a for x in b])
    elif isinstance(a, collections.Iterable) and isinstance(b, collections.Iterable):
        srs.push(_sum([prod(x) for x in izip(a,b,fillvalue=0)]))
    else:
        srs.push(a*b)

def plus_fn(srs):
    a=srs.pop()
    b=srs.pop()
    if isinstance(a, collections.Iterable) ^ isinstance(b, collections.Iterable):
        if isinstance(a, collections.Iterable):
            srs.push([x+b for x in a])
        elif isinstance(b, collections.Iterable):
            srs.push([x+a for x in b])
    elif isinstance(a, collections.Iterable) and isinstance(b, collections.Iterable):
        if isinstance(a, str) and isinstance(b, str):
            srs.push(a+b)
        elif isinstance(a, str):
            srs.push(itertools.chain([a], b))
        elif isinstance(b, str):
            srs.push(itertools.chain(a, [b]))
        else:
            srs.push(itertools.chain(a, b))
    else:
        srs.push(a+b)

@memoize
def digit_to_char(digit, base):
    alphabet = ("0123456789"+string.ascii_uppercase+string.ascii_lowercase+"+/") if base <= 64 else CP437.table
    return alphabet[digit]

@memoize
def char_to_digit(char, base):
    alphabet = ("0123456789"+string.ascii_uppercase+string.ascii_lowercase+"+/") if base <= 64 else CP437.table
    return alphabet.index(char)

@memoize
def str_base(number,base):
    if number < 0:
        return '-' + str_base(-number, base)
    if isinstance(number, float): return str_base_float(number,base,0)
    (d, m) = divmod(number, base)
    if d > 0:
        return str_base(d, base) + digit_to_char(m, base)
    return digit_to_char(m, base)

@memoize
def str_base_float(number,base,exp):
    if number >= base:
        return str_base_float(number/base,base,exp+1)
    if exp<-15 or (number == 0 and exp < 0):            #15 places after the dot should be good, right?
        return ""
    return digit_to_char(int(number), base) + ("." if exp==0 and number%1 else "") + str_base_float((number%1)*base,base,exp-1)

@memoize
def int_base(number,base):
    return reduce(lambda x,y:x*base+y, [char_to_digit(char, base) for char in number], 0)

def i_mul_fn(srs):
    a=srs.pop()
    if isinstance(a, collections.Iterable):
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
        if srs.debug_mode:
            print("islice indices:",b,b+1)
        srs.push([x for x in itertools.islice(a,b,b+1)][0])

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
    srs.stack=deque(tmp[::-1])

def S_fn(srs):
    a=srs.pop()
    if isinstance(a, str):
        srs.push(''.join(sorted(a)))
    elif isinstance(a, collections.Iterable):
        srs.push(sorted(a))
    else:
        srs.push(math.sin(a))

def print_all_fn(srs):
    while srs.stack:
        print(srs.pop())

def zip_fn(srs):
    a=srs.pop()
    if isinstance(a, collections.Iterable):
        b=srs.pop()
        srs.push(zip_longest(a,b))
    else:
        lists = [srs.pop() for i in range(a)]
        srs.push(zip_longest(*lists))

def sum_fn(srs):
    a=[x for x in srs.pop()]
    if len(a) == 0:
        srs.push(0)
    else:
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
    a=[x for x in srs.pop()]
    if len(a)%2:
        srs.push(a[len(a)//2])
    else:
        if all([isinstance(x, str) for x in a[len(a)//2-1:][:2]]):
            med = median(map(ord,a))
            srs.push(chr(int(med)))
        else:
            srs.push(median(a))

def c_fn(srs):
    a=srs.pop()
    if anytype(a, collections.Iterable):
        b=srs.pop()
        srs.push(a.count(b))
    else:
        srs.push(chr(a%256))

def exit_fn(srs):
    exit()

registers = dict()
registers[0] = 0
registers[1] = ""

def get_reg(i):
    global registers
    return registers[i]

def set_reg(i, val):
    global registers
    registers[i] = val

def diff_fn(srs):
    a,b=srs.pop(),srs.pop()
    if all([isinstance(x, collections.Iterable) for x in (a,b)]):
        srs.push([x for x in a if x not in b])
    elif isinstance(a, collections.Iterable):
        srs.push(map(lambda x:x-b, a))
    elif isinstance(b, collections.Iterable):
        srs.push(map(lambda x:a-x, b))
    else:
        srs.push(a-b)

def m_fn(srs):
    a=srs.pop()
    if anytype(a, collections.Iterable):
        srs.push(min(a))
    else:
        srs.push(list(math.modf(a)))

def inv_fil_fn(srs):
    a=srs.pop()
    if srs.debug_mode:
        print("numeric filter on:", a)
    if isinstance(a, collections.Iterable):
        srs.push(filter_types(a, int, float, complex))
    else:
        srs.push(1/a)

def AE_fn(srs):
    a=srs.pop()
    if isinstance(a, str):
        b,c=srs.pop(),srs.pop()
        srs.push(a.replace(b,c))
    else:
        srs.push(filter_types(a, str))

def fn_fil_fn(srs):
    a=srs.pop()
    if isinstance(a, collections.Iterable) and not isinstance(a, str):
        srs.push([x for x in a if isinstance(x, SeriousFunction)])
    else:
        srs.push(SeriousFunction(a))

def get_input_fn(srs):
    a=input()
    b = ast.literal_eval(a)
    srs.inputs.append(b)
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
            a = [x for x in a]
            a[b] = c
        srs.push(a)

def O_fn(srs):
    a = srs.pop()
    if isinstance(a, collections.Iterable):
        a = ''.join(flatten(a))
    srs.push(map(ord,a))

def dig_fn(srs):
    a = srs.pop()
    l = len(srs.stack)
    a = a % l
    srs.stack = [srs.stack[a]]+srs.stack[:a]+srs.stack[a+1:]

def D_fn(srs):
    a = srs.pop()
    if isinstance(a, collections.Iterable) and not isinstance(a, str):
        srs.push(pstdev(a))
    elif isinstance(a, str):
        if len(a) == 1:
            srs.push(chr_cp437(ord_cp437(a)-1%256))
    else:
        srs.push(a-1)

def reg_all_input_fn(srs):
    global registers
    for i,n in enumerate(sys.stdin.read().split('\n')):
        a = ast.literal_eval(n)
        srs.inputs.append(a)
        registers[i] = a


def range_ab_fn(srs):
    a = srs.pop()
    if isinstance(a, collections.Iterable):
        srs.push(range(*[x for x in a]))
    else:
        b = srs.pop()
        srs.push(range(a,b))

def cart_prod_fn(srs):
    a,b = srs.pop(),srs.pop()
    if anytype(b, int, float):
        srs.push(itertools.product(a,repeat=b))
    else:
        srs.push(itertools.product(a,b))

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
        a = srs.pop()
        dd = collections.deque(a, maxlen=1)
        srs.push(dd.pop())

def shuffle_fn(srs):
    a = srs.pop()
    isstr = isinstance(a, str)
    a = [x for x in a]
    random.shuffle(a)
    if isstr:
        a = ''.join(a)
    srs.push(a)

def g_fn(srs):
    a = srs.pop()
    if isinstance(a, collections.Iterable):
        srs.push(gcd_list(*a))
    else:
        b = srs.pop()
        srs.push(gcd(a,b))

def reduce_fn(srs):
    a = srs.pop()
    if isinstance(a, collections.Iterable):
        srs.push([x//gcd_list(*a) for x in a])
    else:
        b = srs.pop()
        srs.push(b//gcd(a,b))
        srs.push(a//gcd(a,b))

def is_unique_fn(srs):
    a = srs.pop()
    srs.push(1 if all(a.count(x) == 1 for x in a) else 0)

def uniquify_fn(srs):
    a = srs.pop()
    unique = [x for i,x in enumerate(a) if i==a.index(x)]
    if isinstance(a, str):
        srs.push(''.join(unique))
    else:
        srs.push(unique)

def binrep(val, pad=None):
    if isinstance(val, int):
        return ("{:0%sb}"%(pad or '')).format(val)
    elif isinstance(val, str):
        if all(ord(x) < 256 for x in val):
            return ''.join(binrep(ord(x), 8) for x in val)
        else:
            raise TypeError
    elif isinstance(val, float):
        return ''.join("{:08b}".format(x) for x in struct.pack('>d',val))
    else:
        raise TypeError

def hexrep(val):
    br = binrep(val)
    res = ''
    for i in range(0, len(br), 8):
        res += hex(int(br[i:i+8],2))[2:]
    return res

def H_fn(srs):
    if not srs.stack:
        srs.push("Hello, World!")
    else:
        a,b = srs.pop(), srs.pop()
        srs.push(a[:b])

def t_fn(srs):
    a,b = srs.pop(), srs.pop()
    if isinstance(b, str):
        c = srs.pop()
        srs.push(a.translate(str.maketrans(b, c)))
    else:
        srs.push(a[b:])

def V_fn(srs):
    a,b = srs.pop(), srs.pop()
    if anytype(a, collections.Iterable):
        res = []
        # get small head lists
        for i in range(1, b):
            res.append(a[:i])
        # get middle lists
        for i in range(len(a)-b+1):
            res.append(a[i:i+b])
        # get small tail lists
        for i in range(b-1, 0, -1):
            res.append(a[-i:])
        if isinstance(a, str):
            res = [''.join(x) for x in res]
        srs.push(res)
    else:
        srs.push(random.uniform(a,b))

def xor(a, b):
    if isinstance(a,str) and isinstance(b,str):
        return ''.join(x for x in a+b if (x in a) ^ (x in b))
    elif isinstance(a,collections.Iterable) and isinstance(b,collections.Iterable):
        return [x for x in a+b if (x in a) ^ (x in b)]
    else:
        return a ^ b

def rrot_fn(srs):
    srs.stack.rotate(-1)

def lrot_fn(srs):
    srs.stack.rotate(1)

def fil_iter_fn(srs):
    a = srs.pop()
    srs.push(filter_types(a, collections.Iterable, exclude=[str]))

def filter_true_fn(srs):
    a,b = srs.pop(), srs.pop()
    if isinstance(a, SeriousFunction):
        res = []
        for x in b:
            s2 = srs.make_new(x)
            aout = a(s2)
            if aout and aout[0]:
                res.append(x)
        srs.push(res)
    else:
        srs.push(itertools.compress(b,a))

def first_n_fn(srs):
    f,n = srs.pop(), srs.pop()
    res = []
    for x in itertools.count(0):
        if len(res) >= n:
            break
        s2 = srs.make_new(x)
        fout = f(s2)
        if fout and fout[0]:
            res.append(x)
    srs.push(res)

def F_fn(srs):
    a = srs.pop()
    if isinstance(a, collections.Iterable):
        srs.push(next(iter(a)))
    else:
        srs.push(Fib(a))

def comp_parts_fn(srs):
    a = srs.pop()
    c = complex(a)
    srs.push(c.real)
    srs.push(c.imag)

def pow_fn(srs):
    a,b = srs.pop(), srs.pop()
    if isinstance(a, collections.Iterable):
        srs.push(map(lambda x:x**b, a))
    else:
        srs.push(pow(a,b))

def Y_fn(srs):
    a = srs.pop()
    if isinstance(a, SeriousFunction):
        last_stack = None
        while last_stack != srs.stack:
            last_stack = srs.stack.copy()
            a(srs)
    else:
        srs.push(0 if a else 1)

def mean_fn(srs):
    a = srs.pop()
    srs.push(mean(a))

def mode_fn(srs):
    a = srs.pop()
    srs.push(mode([x for x in a]))

def add_reg0_fn(srs):
    global registers
    a = srs.pop()
    registers[0] += a

def add_reg1_fn(srs):
    global registers
    a = srs.pop()
    registers[1] += a

def cumsum_fn(srs):
    a = srs.pop()
    sums = []
    for i in range(len(a)):
        sums.append(sum(a[:i+1]))
    srs.push(sums)

def u_fn(srs):
    a = srs.pop()
    if isinstance(a, collections.Iterable) and not isinstance(a, str):
        srs.push(map(lambda x:x+1,a))
    elif isinstance(a, str):
        if len(a) == 1:
            srs.push(chr_cp437(ord_cp437(a)+1%256))
    else:
        srs.push(a+1)

def caret_fn(srs):
    a,b = srs.pop(),srs.pop()
    isstr = isinstance(a, str)
    if isinstance(a, collections.Iterable):
        a = [x for x in a]
        b = [x for x in b]
        xor = [x for x in a+b if (x in a) ^ (x in b)]
        if isstr:
            xor = ''.join(xor)
        srs.push(xor)
    else:
        srs.push(a^b)

def divisors_fn(srs):
    a = srs.pop()
    srs.push([x for x in range(1, a+1) if a%x==0])

def chunk_len_fn(srs):
    a = srs.pop()
    a = [x for x in a] if not isinstance(a, str) else a
    b = srs.pop()
    res = []
    for i in range(0, len(a), b):
        res.append(a[i:i+b])
    srs.push(res)

def chunk_num_fn(srs):
    a = srs.pop()
    a = [x for x in a] if not isinstance(a, str) else a
    b = srs.pop()
    diff = len(a)%b
    chunksize = [len(a)//b+(i<diff) for i in range(b)][::-1]
    i,j = 0,0
    res = []
    while j < len(a):
        res.append(a[j:j+chunksize[i]])
        j += chunksize[i]
        i += 1
    srs.push(res)

def list_repeat_fn(srs):
    a = srs.pop()
    b = srs.pop()
    if isinstance(b, str):
        srs.push([b]*a)
    elif isinstance(b, collections.Iterable):
        srs.push([x for x in b]*a)
    else:
        srs.push([b]*a)

def nth_input_fn(srs):
    a = srs.pop() if len(srs.stack) else 0
    try:
        srs.push(srs.inputs[a])
    except:
        srs.push(a)
        srs.push(srs.inputs[0])

def mu_fn(srs):
    a = srs.pop()
    srs.push(math.sqrt(mean(x**2 for x in a)))

def equal_fn(srs):
    a,b = srs.pop(), srs.pop()
    if isinstance(a, collections.Iterable) and isinstance(b, collections.Iterable):
        srs.push(int(as_list(a) == as_list(b)))
    else:
        srs.push(int(a == b))

def lcm(a, b):
    return a*b//gcd(a,b) if a and b else a or b

def lcm_many(*args):
    return reduce(lcm, args)

def lcm_fn(srs):
    a = srs.pop()
    if isinstance(a, collections.Iterable):
        srs.push(lcm_many(*a) if a else a)
    else:
        b = srs.pop()
        srs.push(lcm(a,b))

def slice_fn(srs):
    a,b = srs.pop(), srs.pop()
    a = list(a) if (isinstance(a, collections.Iterable) and not isinstance(a, str)) else a
    if isinstance(b, collections.Iterable):
        lb = list(b)
        start, stop, step = (b+[None]*3)[:3]
        srs.push(a[slice(start, stop, step)])
    else:
        c,d = srs.pop(), srs.pop()
        srs.push(a[b:c:d])

fn_table={
        0x09:lambda x:x.push(sys.stdin.read(1)),
        0x15:lambda x:x.push(sys.stdin.read()),
        0x1E:lcm_fn,
        0x1F:reduce_fn,
        0x20:lambda x:x.push(len(x.stack)),
        0x21:lambda x:x.push(math.factorial(x.pop())),
        0x23:make_list_fn,
        0x24:lambda x:x.push(str(x.pop())),
        0x25:mod_fn,
        0x26:lambda x:x.push(x.pop() & x.pop()),
        0x28:rrot_fn,
        0x29:lrot_fn,
        0x2A:star_fn,
        0x2B:plus_fn,
        0x2C:get_input_fn,
        0x2D:diff_fn,
        0x2E:print_fn,
        0x2F:div_fn,
        0x3B:dupe_fn,
        0x3C:lambda x:x.push(int(x.pop()<x.pop())),
        0x3D:equal_fn,
        0x3E:lambda x:x.push(int(x.pop()>x.pop())),
        0x3F:lambda x:x,
        0x40:rot2_fn,
        0x41:lambda x:x.push(abs(x.pop())),
        0x42:lambda x:x.push(random.randrange(x.pop(),x.pop())),
        0x43:lambda x:x.push(math.cos(x.pop())),
        0x44:D_fn,
        0x45:E_fn,
        0x46:F_fn,
        0x47:lambda x:x.push(random.random()),
        0x48:H_fn,
        0x49:if_fn,
        0x4A:j_fn,
        0x4B:lambda x:x.push(math.ceil(x.pop())),
        0x4C:lambda x:x.push(math.floor(x.pop())),
        0x4D:M_fn,
        0x4E:N_fn,
        0x4F:O_fn,
        0x50:lambda x:x.push(nth_prime(x.pop())),
        0x51:lambda x:x.push(x.code),
        0x52:R_fn,
        0x53:S_fn,
        0x54:T_fn,
        0x55:lambda x:x.push(list(set(x.pop()).union(x.pop()))),
        0x56:V_fn,
        0x58:lambda x:x.pop(),
        0x59:Y_fn,
        0x5A:zip_fn,
        0x5C:idiv_fn,
        0x5E:caret_fn,
        0x5F:lambda x:x.push(math.log(x.pop())),
        0x61:invert_fn,
        0x62:lambda x:x.push(int(bool(x.pop()))),
        0x63:c_fn,
        0x64:d_fn,
        0x65:lambda x:x.push(math.exp(x.pop())),
        0x66:f_fn,
        0x67:g_fn,
        0x68:lambda x:x.push(math.hypot(x.pop(),x.pop())),
        0x69:i_fn,
        0x6A:lambda x:x.push(str.join(x.pop(),map(str,x.pop()))),
        0x6B:to_list_fn,
        0x6C:lambda x:x.push(len(x.pop())),
        0x6D:m_fn,
        0x6E:n_fn,
        0x6F:psh_fn,
        0x70:p_fn,
        0x71:enq_fn,
        0x72:lr_fn,
        0x73:s_fn,
        0x74:t_fn,
        0x75:u_fn,
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
        0x91:mean_fn,
        0x92:AE_fn,
        0x93:lambda x:x.push(x.pop().strip()),
        0x94:lambda x:x.push(x.pop().lstrip()),
        0x95:lambda x:x.push(x.pop().rstrip()),
        0x96:lambda x:x.push(x.pop().upper()),
        0x97:lambda x:x.push(x.pop().lower()),
        0x98:lambda x:x.push(x.pop().title()),
        0x99:lambda x:x.push(x.pop().swapcase()),
        0x9A:mode_fn,
        0x9B:lambda x:x.push(math.copysign(x.pop(),x.pop())),
        0x9C:fn_fil_fn,
        0x9D:lambda x:x.push([a+b for a,b in itertools.zip_longest(x.pop(),x.pop(),fillvalue=0)]),
        0x9E:lambda x:x.push(cmath.phase(x.pop())),
        0x9F:lambda x:SeriousFunction(x.pop())(x),
        0xA0:lambda x:x.push(x.pop().conjugate()),
        0xA1:index_fn,
        0xA2:cond_quit_fn,
        0xA3:lambda x:x.push(''.join(map(chr,range(97,122+1)))),
        0xA4:lambda x:x.push(map(list,enumerate(x.pop()))),
        0xA5:fil_iter_fn,
        0xA7:lambda x:x.push(math.degrees(x.pop())),
        0xA8:lambda x:x.push(int_base(''.join(map(str,x.pop())),x.pop())),
        0xA9:lambda x:x.push(x.pop()+2),
        0xAA:lambda x:x.push(x.pop()-2),
        0xAB:lambda x:x.push(x.pop()/2),
        0xAC:lambda x:x.push(x.pop()/4),
        0xAD:lambda x:x.push(str_base(x.pop(),x.pop())),
        0xAE:ins_bot_fn,
        0xAF:ins_top_fn,
        0xB0:filter_true_fn,
        0xB1:lambda x:x.push((lambda y:sum([1 if gcd(i,y)==1 else 0 for i in range(1,y+1)]))(x.pop())),
        0xB2:prime_count_fn,
        0xB3:dupe_all_fn,
        0xB4:lambda x:x.push(1 if gcd(x.pop(),x.pop())==1 else 0),
        0xB5:chunk_num_fn,
        0xB7:add_reg0_fn,
        0xB8:add_reg1_fn,
        0xB9:lambda x:x.push((lambda y:[nCr(y,k) for k in range(y+1)])(x.pop())),
        0xBA:median_fn,
        0xBB:lambda x:set_reg(0,x.pop()),
        0xBC:lambda x:set_reg(1,x.pop()),
        0xBD:lambda x:x.push(get_reg(0)),
        0xBE:lambda x:x.push(get_reg(1)),
        0xBF:lambda x:set_reg(x.pop(),x.pop()),
        0xC0:lambda x:x.push(get_reg(x.pop())),
        0xC2:lambda x:x.push(list(zip(*x.pop()))),
        0xC3:lambda x:x.push(binrep(x.pop())),
        0xC4:lambda x:x.push(hexrep(x.pop())),
        0xC5:dupe_each_fn,
        0xC6:dupe_each_n_fn,
        0xC7:npop_list_fn,
        0xC8:shuffle_fn,
        0xC9:uniquify_fn,
        0xCA:reg_all_input_fn,
        0xCB:lambda x:x.push(math.pi),
        0xCC:lambda x:x.push(math.e),
        0xCD:is_unique_fn,
        0xCE:while_fn,
        0xCF:lambda x:x.push(itertools.combinations(x.pop(),x.pop())),
        0xD0:lambda x:x.push(itertools.permutations(x.pop(),x.pop())),
        0xD1:lambda x:x.push(pow(10,x.pop())),
        0xD2:lambda x:x.push(math.log(x.pop(),10)),
        0xD3:lambda x:x.push(pow(2,x.pop())),
        0xD4:lambda x:x.push(math.log(x.pop(),2)),
        0xD5:lambda x:x.push(math.log(2)),
        0xD6:first_n_fn,
        0xD7:comp_parts_fn,
        0xD8:chunk_len_fn,
        0xD9:lambda x:x.push(ord_cp437(x.pop())),
        0xDA:lambda x:x.push(chr_cp437(x.pop())),
        0xDB:lambda x:x.push(nCr(x.pop(),x.pop())),
        0xDC:lambda x:x.push(nPr(x.pop(),x.pop())),
        0xDD:lambda x:x.push(b64decode(x.pop().encode('cp437')).decode('cp437')),
        0xDE:lambda x:x.push(b64encode(x.pop().encode('cp437')).decode('cp437')),
        0xDF:lambda x:x.push(("0123456789"+string.ascii_uppercase+string.ascii_lowercase+"+/")[:x.pop()]),
        0xE0:list_repeat_fn,
        0xE1:nth_input_fn,
        0xE2:lambda x:x.push(math.gamma(x.pop())),
        0xE3:lambda x:x.push(reduce(operator.mul,x.pop(),1)),
        0xE4:sum_fn,
        0xE5:cumsum_fn,
        0xE6:mu_fn,
        0xE7:lambda x:x.push(x.pop()*2),
        0xE8:slice_fn,
        0xEB:dig_fn,
        0xEC:lambda x:x.toggle_preserve(),
        0xED:lambda x:x.push(phi),
        0xEE:lambda x:x.push(""),
        0xEF:lambda x:x.push(list(set(x.pop()).intersection(x.pop()))),
        0xF0:lambda x:x.push(eval(x.pop())),
        0xF1:lambda x:x.push(-x.pop()),
        0xF2:lambda x:x.push(x.pop()>=x.pop()),
        0xF3:lambda x:x.push(x.pop()<=x.pop()),
        0xF6:divisors_fn,
        0xF7:lambda x:x.push(int(x.pop())),
        0xF8:lambda x:x.push(math.radians(x.pop())),
        0xF9:cart_prod_fn,
        0xFB:lambda x:x.push(x.pop()**.5),
        0xFC:pow_fn,
        0xFD:lambda x:x.push(x.pop()**2),
        0xFE:peek_print_fn,
}
