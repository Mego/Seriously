#!/usr/bin/env python3

import re

def regex_matches_fn(srs):
    pattern = srs.pop()
    string = srs.pop()
    srs.push(1 if re.match(pattern, string) else 0)

fn_table = {
    0x4D: regex_matches_fn,
}