#!/usr/bin/env python3

from copy import copy
from functools import wraps
from collections import Iterable

def wrap(obj):
    # TODO: use proper classes for each category
    if isinstance(obj, (int, float, complex)):
        return SeriousNumeric(obj)
    elif isinstance(obj, str):
        return SeriousString(obj)
    elif isinstance(obj, bytes):
        return SeriousString(obj.decode())
    elif isinstance(obj, Iterable):
        return SeriousIterable(obj)
    elif not isinstance(obj, SeriousObject):
        return SeriousObject(obj)
    else:
        return obj

def reflect_binary(f):
    @wraps(f)
    def f_reflect(x, y):
        return f(y, x)
    return f_reflect
    
def wrap_fn(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return wrap(f(*args, **kwargs))
    return wrapper
    
def set_self(f):
    @wraps(f)
    def wrapper(obj, other):
        return obj.set(f(obj, other).value())
    return wrapper

class SeriousObject:
    def __init__(self, obj):
        self.obj = obj

    def value(self):
        return self.obj

    def set(self, obj):
        self.obj = obj
        return self

    @wrap_fn
    def copy(self):
        return copy(self.value())

    def __bool__(self):
        return bool(self.value())

    def __repr__(self):
        return repr(self.value())

    @wrap_fn
    def __str__(self):
        return str(self.value())

class SeriousNumeric(SeriousObject):
    def __init__(self, obj):
        super().__init__(obj)

    def __lt__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() < other.value())
        else:
            try:
                return self < wrap(other)
            except:
                return NotImplemented

    def __eq__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() == other.value())
        else:
            try:
                return self == wrap(other)
            except:
                return NotImplemented

    def __gt__(self, other):
        try:
            return other < self
        except:
            try:
                return self > wrap(other)
            except:
                return NotImplemented

    def __le__(self, other):
        try:
            return SeriousNumeric(not bool(self > other))
        except:
            try:
                return self <= wrap(other)
            except:
                return NotImplemented

    def __ge__(self, other):
        try:
            return SeriousNumeric(not bool(self < other))
        except:
            try:
                return self >= wrap(other)
            except:
                return NotImplemented

    def __add__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() + other.value())
        else:
            try:
                return self + wrap(other)
            except:
                return NotImplemented

    def __sub__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() - other.value())
        else:
            try:
                return self - wrap(other)
            except:
                return NotImplemented

    def __mul__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() * other.value())
        else:
            try:
                return self * wrap(other)
            except:
                return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() / other.value())
        else:
            try:
                return self / wrap(other)
            except:
                return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() // other.value())
        else:
            try:
                return self // wrap(other)
            except:
                return NotImplemented

    def __mod__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() % other.value())
        else:
            try:
                return self % wrap(other)
            except:
                return NotImplemented

    def __divmod__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(divmod(self.value(), other.value()))
        else:
            try:
                return divmod(self, wrap(other))
            except:
                return NotImplemented

    def __pow__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() ** other.value())
        else:
            try:
                return self ** wrap(other)
            except:
                return NotImplemented

    def __lshift__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() << other.value())
        else:
            try:
                return self << wrap(other)
            except:
                return NotImplemented

    def __rshift__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() >> other.value())
        else:
            try:
                return self >> wrap(other)
            except:
                return NotImplemented

    def __and__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() & other.value())
        else:
            try:
                return self & wrap(other)
            except:
                return NotImplemented

    def __or__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() | other.value())
        else:
            try:
                return self | wrap(other)
            except:
                return NotImplemented

    def __xor__(self, other):
        if isinstance(other, SeriousNumeric):
            return SeriousNumeric(self.value() ^ other.value())
        else:
            try:
                return self ^ wrap(other)
            except:
                return NotImplemented

    __radd__ = reflect_binary(__add__)
    __rsub__ = reflect_binary(__sub__)
    __rmul__ = reflect_binary(__mul__)
    __rtruediv__ = reflect_binary(__truediv__)
    __rfloordiv__ = reflect_binary(__floordiv__)
    __rmod__ = reflect_binary(__mod__)
    __rdivmod__ = reflect_binary(__divmod__)
    __rpow__ = reflect_binary(__pow__)
    __rlshift__ = reflect_binary(__lshift__)
    __rrshift__ = reflect_binary(__rshift__)
    __rand__ = reflect_binary(__and__)
    __ror__ = reflect_binary(__or__)
    __rxor__ = reflect_binary(__xor__)
    
    __iadd__ = set_self(__add__)
    __isub__ = set_self(__sub__)
    __imul__ = set_self(__mul__)
    __itruediv__ = set_self(__truediv__)
    __ifloordiv__ = set_self(__floordiv__)
    __imod__ = set_self(__mod__)
    __idivmod__ = set_self(__divmod__)
    __ipow__ = set_self(__pow__)
    __ilshift__ = set_self(__lshift__)
    __irshift__ = set_self(__rshift__)
    __iand__ = set_self(__and__)
    __ior__ = set_self(__or__)
    __ixor__ = set_self(__xor__)
    
    def __neg__(self):
        return SeriousNumeric(-self.value())

    def __pos__(self):
        return SeriousNumeric(+self.value())

    def __abs__(self):
        return SeriousNumeric(abs(self.value()))

    def __invert__(self):
        return SeriousNumeric(~self.value())

    def __complex__(self):
        return complex(self.value())

    def __int__(self):
        return int(self.value())

    def __float__(self):
        return float(self.value())

    def __round__(self, n=None):
        return round(self.value(), n)

    def __index__(self):
        if isinstance(self.value(), int):
            return int(self)
        else:
            return NotImplemented

class SeriousIterable(SeriousObject):
    pass

class SeriousString(SeriousIterable):
    pass

if __name__ == '__main__':
    print(SeriousObject(4)+SeriousNumeric(4))