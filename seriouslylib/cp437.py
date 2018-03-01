#!/usr/bin/env python3

class CP437():
    table = (
    '\x00\u263a\u263b\u2665\u2666\u2663\u2660\u2022\u25d8\u25cb\u25d9'
    '\u2642\u2640\u266a\u266b\u263c\u25ba\u25c4\u2195\u203c\xb6\xa7'
    '\u25ac\u21a8\u2191\u2193\u2192\u2190\u221f\u2194\u25b2\u25bc !"'
    +r"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]"
    +'^_`abcdefghijklmnopqrstuvwxyz{|}~\u2302\xc7\xfc\xe9\xe2\xe4\xe0'
    '\xe5\xe7\xea\xeb\xe8\xef\xee\xec\xc4\xc5\xc9\xe6\xc6\xf4\xf6\xf2'
    '\xfb\xf9\xff\xd6\xdc\xa2\xa3\xa5\u20a7\u0192\xe1\xed\xf3\xfa\xf1'
    '\xd1\xaa\xba\xbf\u2310\xac\xbd\xbc\xa1\xab\xbb\u2591\u2592\u2593'
    '\u2502\u2524\u2561\u2562\u2556\u2555\u2563\u2551\u2557\u255d'
    '\u255c\u255b\u2510\u2514\u2534\u252c\u251c\u2500\u253c\u255e'
    '\u255f\u255a\u2554\u2569\u2566\u2560\u2550\u256c\u2567\u2568'
    '\u2564\u2565\u2559\u2558\u2552\u2553\u256b\u256a\u2518\u250c'
    '\u2588\u2584\u258c\u2590\u2580\u03b1\xdf\u0393\u03c0\u03a3\u03c3'
    '\xb5\u03c4\u03a6\u0398\u03a9\u03b4\u221e\u03c6\u03b5\u2229\u2261\xb1'
    '\u2265\u2264\u2320\u2321\xf7\u2248\xb0\u2219\xb7\u221a\u207f\xb2\u25a0\xa0'
    )


    @staticmethod
    def ord(c):
        return CP437.table.find(c)


    @staticmethod
    def chr(o):
        if not 0 <= o < 256:
            raise ValueError
        return CP437.table[o]


    @staticmethod
    def from_Unicode(s):
        res = []
        for c in s:
            if c in CP437.table:
                res.append(CP437.ord(c))
            else:
                res.extend(c.encode('utf-8'))
        return res
