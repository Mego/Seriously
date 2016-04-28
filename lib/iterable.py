#!/usr/bin/env python3

from collections.abc import Iterable

def as_list(val, wrap=True):
    if not isinstance(val, Iterable):
        return [val] if wrap else val
    else:
        return [as_list(x, wrap=False) for x in val]