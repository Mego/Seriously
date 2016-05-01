#!/usr/bin/env python3

from collections import deque as _deque
from collections.abc import Iterable
from itertools import islice, chain, repeat

def as_list(val, wrap=True):
    #strings are iterables all the way down, so an exception needs to be made
    # else we get infinite recursion, which is bad
    # this only took me 2 hours to debug, new record!
    if not isinstance(val, Iterable) or isinstance(val, str):
        return [val] if wrap else val
    else:
        return [as_list(x, wrap=False) for x in val]
        
class deque(_deque):
    def copy(self):
        if hasattr(_deque, 'copy'):
            return _deque.copy(self)
        else:
            return deque(x for x in self)
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            return islice(self, key.start, key.stop, key.step)
        else:
            return _deque.__getitem__(self, key)
            
    def reversed(self):
        tmp = self.copy()
        tmp.reverse()
        return tmp
        
    def __add__(self, other):
        if hasattr(_deque, 'add'):
            return _deque.__add__(self, other)
        else:
            tmp = self.copy()
            tmp.extend(other)
            return tmp
            
    __radd__ = __add__
    
def zip_longest(*iterables):
    its = [iter(x) for x in iterables]
    res = []
    for it in its:
        n = next(it, None)
        if n is not None:
            res.append(n)
    while res:
        yield res
        res = []
        for it in its:
            n = next(it, None)
            if n is not None:
                res.append(n)