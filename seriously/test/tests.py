#!/usr/bin/env python3
import argparse
import collections
import contextlib
import math
import random
from io import StringIO
import sys
import unittest
from seriouslylib.cp437 import CP437
from seriouslylib.iterable import as_list
from seriouslylib.nicenames import nice_names
from ..seriously import Seriously, minimize
from ..SeriouslyCommands import SeriousFunction
from ..probably_prime import probably_prime

ord_cp437 = CP437.ord
chr_cp437 = CP437.chr

debug_mode = False

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


class UtilTests(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        # fix for Python < 3.4
        if not hasattr(self, 'subTest'):
            self.subTest = self.dummy_manager
    
    @contextlib.contextmanager
    def dummy_manager(*args, **kwargs):
        yield

    def test_utils(self):
        self.assertEqual(as_list(range(5)), [0, 1, 2, 3, 4])
        self.assertEqual(as_list((1,2,3,4) for x in range(3)), [[1, 2, 3, 4]]*3)
        self.assertEqual(as_list(2), [2])
        self.assertEqual([chr_cp437(x) for x in range(256)], [x for x in CP437.table])
        self.assertEqual([ord_cp437(x) for x in CP437.table], [x for x in range(256)])
        with self.assertRaises(ValueError):
            chr_cp437(257)
        self.assertEqual(CP437.from_Unicode(chr_cp437(0x8D)+'\u2266'), [0x8D, 0xE2, 0x89, 0xA6])
        
    def test_seriously_class(self):
        srs = Seriously()
        srs.push(1)
        srs.prepend(0)
        self.assertEqual(srs.stack, collections.deque([0, 1]))
    
    def test_nice_names(self):
        for i, nice_name in enumerate(nice_names):
            with self.subTest(i=i):
                self.assertEqual(minimize(nice_name), chr_cp437(nice_names[nice_name]))
        self.assertEqual(minimize("3 copy add square half"), "3;+²½")


class SeriousTest(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        # fix for Python < 3.4
        if not hasattr(self, 'subTest'):
            self.subTest = self.dummy_manager

    @contextlib.contextmanager
    def dummy_manager(*args, **kwargs):
        yield

    def setUp(self):
        self.srs = Seriously(debug_mode=debug_mode)

    def tearDown(self):
        self.srs = None
        if sys.stdin is not sys.__stdin__:
            sys.stdin.close()
            sys.stdin = sys.__stdin__

    def setInput(self, str):
        if sys.stdin is not sys.__stdin__:
            sys.stdin.close()
        sys.stdin = StringIO(str)

    def assert_serious(self, code, output, input=None, close=False):
        if input is not None:
            self.setInput(input)
        else:
            self.setInput('')
        if not close:
            self.assertEqual(self.srs.eval(code), output)
        else:
            for a, b in zip(self.srs.eval(code), output):
                self.assertAlmostEqual(a, b)
        self.srs.clear_stack()


class IOTests(SeriousTest):
    def test_raw_input(self):
        self.assert_serious(chr_cp437(0x09), ['a'], "a\n")
        self.assert_serious(chr_cp437(0x15), ['abc\n'], "abc\n")

    def test_formatted_input(self):
        self.assert_serious(',', ['a'], '"a"\n')

        self.assert_serious(',', [12345], '12345\n')

        self.assert_serious(',', [[3, 2, 1]], '[3,2,1]\n')

        self.assert_serious(',', [[3, 2, 1]], '3, 2, 1\n')
        
    def test_implicit_input(self):
        self.assert_serious('', ['a'], '"a"\n')
        
    def test_nth_input(self):
        self.assert_serious(chr_cp437(0xE1), ['a','a'], '"a"\n')
        self.assert_serious('0'+chr_cp437(0xE1), ['a','b','a'], '"a"\n"b"\n')
        self.assert_serious("'r"+chr_cp437(0xE1), ['a', 'r', 'a'], '"a"\n')


class LiteralTests(SeriousTest):
    def test_strings(self):
        self.assert_serious('"a', ['a'])

        self.assert_serious('"a"', ['a'])

        self.assert_serious("'a", ['a'])

        self.assert_serious("'a'b", ['b', 'a'])

    def test_digits(self):
        for i in range(10):
            with self.subTest(i=i):
                self.assert_serious(str(i), [i])

    def test_numerics(self):
        self.assert_serious(':12345', [12345])

        self.assert_serious(':-1', [-1])

        self.assert_serious(':.5', [0.5])

        self.assert_serious(':1+2.2i', [1+2.2j])
        self.assert_serious(':12+', [12])
        self.assert_serious(':+', [0])

    def test_functions(self):
        self.assert_serious("`f", [SeriousFunction("f")])
        self.assert_serious("⌠foo⌡", [SeriousFunction("foo")])
        self.assert_serious("⌠⌠foo⌡⌡", [SeriousFunction("⌠foo⌡")]),
        self.assert_serious("⌠foo⌡$", ["foo"])

    @unittest.skip("eval is banned on this branch")
    def test_eval(self):
        self.assert_serious('"len(set([1,2,2,3]))"{}'.format(chr_cp437(0xF0)),
                            [3])
                            
    def test_lists(self):
        self.assert_serious("[1,2,3]", [[1,2,3]])
        self.assert_serious("[[1],[2]]", [[[1],[2]]])


class StackTests(SeriousTest):
    def test_count(self):
        self.assert_serious('1 ', [1, 1])
        
    def test_dupe(self):
        self.assert_serious('1;', [1, 1])
        self.assert_serious('"abc";', ["abc", "abc"])
        self.assert_serious('3R;', [[1, 2, 3], [1, 2, 3]])
        self.assert_serious('3R;Z;', [[[1,1], [2,2], [3,3]], [[1,1], [2,2], [3,3]]])

    def test_rotations(self):
        self.assert_serious('123(', [1, 3, 2])
        self.assert_serious('123)', [2, 1, 3])
        self.assert_serious('123@', [2, 3, 1])
        self.assert_serious('1232{', [2, 1, 3])
        self.assert_serious('1232}', [1, 3, 2])
        self.assert_serious('13422'+chr_cp437(0xAF), [4,2,3,1])
        self.assert_serious('13422'+chr_cp437(0xAE), [4,3,2,1])
        
    def test_logic(self):
        self.assert_serious(r'120I', [1])
        
    def test_repeat(self):
        self.assert_serious('1;', [1,1])
        self.assert_serious('23n', [3,3])

    def test_quine(self):
        self.assert_serious('Q;', ['Q;', 'Q;'])

    def test_loop(self):
        self.assert_serious('5W;D', [0, 1, 2, 3, 4, 5])

    def test_misc(self):
        self.assert_serious('123a', [1, 2, 3])
        with self.assertRaises(SystemExit):
            self.srs.eval('123'+chr_cp437(0x7F))
        self.srs.clear_stack()
        self.assert_serious('123'+chr_cp437(0xB3), [3, 2, 1, 3, 2, 1])
        self.assert_serious('123'+chr_cp437(0xC5), [3, 3, 2, 2, 1, 1])
        self.assert_serious('12'+chr_cp437(0xC6), [1, 1])
        self.assert_serious('1'+chr_cp437(0xEC)+'D', [0, 1])
        self.assert_serious('N', [NinetyNineBottles()])

    def test_repeat(self):
        self.assert_serious('3¶5', [5, 5, 5])
        self.assert_serious('52¶²', [5**4])

    def test_fork(self):
        self.assert_serious('23♫+-', [[5, 1]])
        self.assert_serious('23♫k*', [[[2, 3], 6]])


class RegisterTests(SeriousTest):
    def test_push_pop(self):
        self.assert_serious('1{}2{}{}{}'.format(
                            chr_cp437(0xBB), chr_cp437(0xBC),
                            chr_cp437(0xBE), chr_cp437(0xBD)), [1, 2])
        self.assert_serious('53{}3{}'.format(chr_cp437(0xBF),
                                             chr_cp437(0xC0)), [5])

    def test_push_iterable(self):
        self.assert_serious('"abc"O╗3R⌠╜@⌡M', [[1, [97, 98, 99], 2, [97, 98, 99], 3, [97, 98, 99]]])

    def test_input(self):
        self.assert_serious(chr_cp437(0xCA)+chr_cp437(0xBD)+chr_cp437(0xBE),
                            [2, 'b'],
                            '"b"\n2\n')


class MathTests(SeriousTest):
    def test_arithmetic(self):
        self.assert_serious('23+', [5])
        self.assert_serious('23-', [1])
        self.assert_serious('23*', [6])
        self.assert_serious('24\\', [2])
        self.assert_serious('25/', [2.5])
        self.assert_serious('25\\', [2])
        self.assert_serious('4'+chr_cp437(0xFD), [16])
        self.assert_serious('32'+chr_cp437(0xFC), [8])
        self.assert_serious('36'+chr_cp437(0x1F), [2, 1])
        self.assert_serious('4!', [24])
        self.assert_serious('24'+chr_cp437(0xDB), [6])
        self.assert_serious('24'+chr_cp437(0xDC), [12])
        self.assert_serious('21'+chr_cp437(0x80), [1+2j])
        self.assert_serious(':12w', [[[2,2],[3,1]]])
        self.assert_serious(':12y', [[2,3]])
        self.assert_serious(':12o', [[2, 2, 3]])
        self.assert_serious(':-3s', [-1])
        self.assert_serious('3s', [1])
        self.assert_serious('0s', [0])
        self.assert_serious('25^', [7])
        self.assert_serious('24%', [0])
        self.assert_serious('3Ru', [[2,3,4]])
        self.assert_serious('[1,2,3]3+', [[4,5,6]])
        self.assert_serious('3R3+', [[4,5,6]])
        self.assert_serious('2[2,4,6]+', [[4, 6, 8]])
        self.assert_serious('23R2*+', [[4, 6, 8]])
        self.assert_serious('[1,2,3]3*', [[3,6,9]])
        self.assert_serious('3R3*', [[3,6,9]])
        self.assert_serious('2[2,4,6]*', [[4, 8, 12]])
        self.assert_serious('23R2**', [[4, 8, 12]])
        self.assert_serious('2'+chr_cp437(0x8C), [2j])
        self.assert_serious('[2,3]'+chr_cp437(0x8C), [[2j,3j]])
        self.assert_serious('2Ru'+chr_cp437(0x8C), [[2j,3j]])
        self.assert_serious(':1+2j'+chr_cp437(0xD7), [2, 1])
        self.assert_serious('6:21▲', [42])
        # weird prime bug test
        self.assert_serious('9uyX9uR`p░', [[2, 3, 5, 7]])
        self.assert_serious(':2.7!', [4.170651783796603], close=True)

    def test_lists(self):
        self.assert_serious('[1][1,2]-', [[2]])
        self.assert_serious('1R2R-', [[2]])
        self.assert_serious('[2,3];*', [13])
        self.assert_serious('3R;*', [14])
        self.assert_serious('[1,2,3]M', [3])
        self.assert_serious('3RM', [3])
        self.assert_serious('[1,2,3]m', [1])
        self.assert_serious('3Rm', [1])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0xE4), [10])
        self.assert_serious('4R'+chr_cp437(0xE4), [10])
        self.assert_serious('[2.5,2.5]'+chr_cp437(0xE4), [5.0])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0xE3), [24])
        self.assert_serious('4R'+chr_cp437(0xE3), [24])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0xBA), [2.5])
        self.assert_serious('4R'+chr_cp437(0xBA), [2.5])
        self.assert_serious('[1,2,6,3,4]'+chr_cp437(0xBA), [6])
        self.assert_serious('5R'+chr_cp437(0xBA), [3])
        self.assert_serious('[1,2,3,3]'+chr_cp437(0x9A), [3])
        self.assert_serious('33Rik'+chr_cp437(0x9A), [3])
        self.assert_serious('[3,6,9,12]'+chr_cp437(0x1F), [[1, 2, 3, 4]])
        self.assert_serious('4R3*'+chr_cp437(0x1F), [[1, 2, 3, 4]])
        self.assert_serious('4r', [[0,1,2,3]])
        self.assert_serious('4R', [[1,2,3,4]])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0x80), [3+4j, 1+2j])
        self.assert_serious('4R'+chr_cp437(0x80), [3+4j, 1+2j])
        self.assert_serious('[1,2,3,4,5]'+chr_cp437(0x80), [5, 3+4j, 1+2j])
        self.assert_serious('5R'+chr_cp437(0x80), [5, 3+4j, 1+2j])
        self.assert_serious('2[1,2,3]'+chr_cp437(0xFC), [[1, 4, 9]])
        self.assert_serious('23R'+chr_cp437(0xFC), [[1, 4, 9]])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0x91), [2.5])
        self.assert_serious('4R'+chr_cp437(0x91), [2.5])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0xE5), [[1, 3, 6, 10]])
        self.assert_serious('4R'+chr_cp437(0xE5), [[1, 3, 6, 10]])
        self.assert_serious('[1,2,3]3R=', [1])
        self.assert_serious('[65,66,67]"ABC"O=', [1])
        self.assert_serious('2Rx', [[1]])
        self.assert_serious('"ABC"OΣ', [65+66+67])
        self.assert_serious('4RΣ', [1+2+3+4])
        self.assert_serious('3r:65+"ABC"O=', [1])
        self.assert_serious('[8,9,21]▲', [504])
        self.assert_serious('[42]▲', [42])
        self.assert_serious('[]▲', [[]])
        self.assert_serious('3R⌐', [[3, 4, 5]])
        self.assert_serious('3R¬', [[-1, 0, 1]])

    def test_filters(self):
        self.assert_serious("[4]12'3k"+chr_cp437(0x8D), [[1, 2]])
        self.assert_serious("[4]12'3k"+chr_cp437(0x92), [['3']])
        self.assert_serious("[4]12'3k"+chr_cp437(0xA5), [[[4]]])

    def test_sequences(self):
        self.assert_serious('2:547*p', [0])
        self.assert_serious(':23p', [1])
        self.assert_serious(':100P', [547])
        self.assert_serious('8f', [6])
        self.assert_serious(':16'+chr_cp437(0xDF), ['0123456789ABCDEF'])
        self.assert_serious('2'+chr_cp437(0xB9), [[1, 2, 1]])
        self.assert_serious(':12F', [144])
        self.assert_serious(':20F', [6765])
        self.assert_serious(':38F', [39088169])
        self.assert_serious(':50'+chr_cp437(0xF6), [[1, 2, 5, 10, 25, 50]])
        self.assert_serious('5'+chr_cp437(0xF6), [[1, 5]])
        self.assert_serious(':10▓', [4])
        self.assert_serious(':15▓', [6])

    def test_trig(self):
        trig_fns = {
            'sin': ('S', chr_cp437(0x83)),
            'sinh': (chr_cp437(0x8E), chr_cp437(0x87)),
            'cos': ('C', chr_cp437(0x84)),
            'cosh': (chr_cp437(0x8F), chr_cp437(0x88)),
            'tan': ('T', chr_cp437(0x85)),
            'tanh': (chr_cp437(0x90), chr_cp437(0x89)),
        }
        for fn in trig_fns:
            with self.subTest(function=fn):
                fns = trig_fns[fn]
                self.assert_serious('1{}{}'.format(*fns), [1], close=True)
                if fn not in ('sinh', 'cosh', 'tanh'):
                    #skip hyperbolic functions for complex because they don't work right
                    # maybe some time in the future I'll learn enough math to make these tests work
                    self.assert_serious(':1+2j{}{}'.format(*fns), [1+2j], close=True)

    def test_complex(self):
        self.assert_serious('[1+2j,2+1j]Σ', [3+3j])
        self.assert_serious('[1+2j,2+1j]π', [5j])
        self.assert_serious('[1+2j,2+1j]σ', [[1+2j, 3+3j]])
        self.assert_serious('[1+2j,2+1j]µ', [complex(math.sqrt(2), math.sqrt(2))], close=True)
        self.assert_serious('[1+2j,2+1j]æ', [1.5+1.5j])


class StringAndListTests(SeriousTest):
    def test_format(self):
        self.assert_serious('[2,3]"{}.{}"f', ["2.3"])
        self.assert_serious('3R"{}.{}{}"f', ["1.23"])
        self.assert_serious('[2,3]"%d.%d"%', ["2.3"])
        self.assert_serious('3R"%d.%d%d"%', ["1.23"])

    def test_modify(self):
        self.assert_serious('52[2,3,4]T', [[2, 3, 5]])
        self.assert_serious('523RuT', [[2, 3, 5]])
        self.assert_serious('52"234"T', ["235"])

    def test_ords(self):
        self.assert_serious('"abc"O', [[0x61, 0x62, 0x63]])
        self.assert_serious('9'+chr_cp437(0xDA), [chr_cp437(0x09)])
        self.assert_serious("'"+chr_cp437(0x09)+chr_cp437(0xD9), [9])

    def test_string_methods(self):
        self.assert_serious('"ab"2*', ["abab"])
        self.assert_serious('"ab"0DD*', ["baba"])
        self.assert_serious('" ab c "'+chr_cp437(0x93), ["ab c"])
        self.assert_serious('" ab c "'+chr_cp437(0x94), ["ab c "])
        self.assert_serious('" ab c "'+chr_cp437(0x95), [" ab c"])
        self.assert_serious('"CAFE babe 123"'+chr_cp437(0x96),
                            ["CAFE BABE 123"])
        self.assert_serious('"CAFE babe 123"'+chr_cp437(0x97),
                            ["cafe babe 123"])
        self.assert_serious('"CAFE babe 123"'+chr_cp437(0x98),
                            ["Cafe Babe 123"])
        self.assert_serious('"CAFE babe 123"'+chr_cp437(0x99),
                            ["cafe BABE 123"])
        self.assert_serious('"abcd"N', ["d"])
        self.assert_serious('"abcd"F', ["a"])
        self.assert_serious("""'0"010203040"s""", [['', '1', '2', '3', '4', '']])
        self.assert_serious('4"Hello"H', ['Hell'])
        self.assert_serious('1"Hello"t', ['ello'])
        self.assert_serious('2"1234"V', [['1', '12', '23', '34', '4']])
        self.assert_serious('"123""345"^', ['4512'])
        self.assert_serious('" A""_a""abc_def"t', ['Abc def'])
        self.assert_serious('"abc"p', ['a', 'bc'])
        self.assert_serious('"abc"d', ['c', 'ab'])
        self.assert_serious('\'d"abc"q', ['abcd'])
        self.assert_serious('\'a"bcd"o', ['abcd'])
        self.assert_serious('"abcd"'+chr_cp437(0x8A), ["'abcd'"])
        self.assert_serious(':123.45'+chr_cp437(0x8A), ['123.45'])
        self.assert_serious(':1+2i'+chr_cp437(0x8A), ['(1+2j)'])
        self.assert_serious('⌠foo⌡'+chr_cp437(0x8A), ['⌠foo⌡'])
        self.assert_serious('"1.23"i', [1.23])
        self.assert_serious('"123"R', ["321"])
        self.assert_serious('"abc"3*', ['abcabcabc'])
        self.assert_serious('3"abc"*', ['abcabcabc'])
        self.assert_serious('3"1234"'+chr_cp437(0xD8), [['123', '4']])
        self.assert_serious('3"1234"'+chr_cp437(0xB5), [['1', '2', '34']])
        self.assert_serious('"abc"3'+chr_cp437(0xE0), [["abc", "abc", "abc"]])
        self.assert_serious('53'+chr_cp437(0xE0), [[5, 5, 5]])
        self.assert_serious("' u", ['!'])
        self.assert_serious("'!D", [' '])
        self.assert_serious('240"abcdef"'+chr_cp437(0xE8), ["ac"])
        self.assert_serious('[0,4,2]"abcdef"'+chr_cp437(0xE8), ["ac"])
        self.assert_serious("3R'.*", [['.', '..', '...']])
        self.assert_serious("{}±".format('''"'foo'"'''), ['"foo"'])
        self.assert_serious("{}±±".format('''"'foo'"'''), ["'foo'"])
        self.assert_serious('"45""12345"í', [3])
        self.assert_serious('"1""0101010"╢', [5])
        
    def test_list_methods(self):
        self.assert_serious('[1,2,3][4,5,6]'+chr_cp437(0x9D), [[5, 7, 9]])
        self.assert_serious('3R;3+'+chr_cp437(0x9D), [[5, 7, 9]])
        self.assert_serious('3R5#+', [[5, 1, 2, 3]])
        self.assert_serious('3R"abc"+', [["abc", 1, 2, 3]])
        self.assert_serious("""'0"010203040"#s""", [[[],['1'],['2'],['3'],['4'],[]]])
        self.assert_serious('0"10203"s', [['1', '2', '3']])
        self.assert_serious('2[1,2,3,4]V', [[[1],[1,2,],[2,3],[3,4],[4]]])
        self.assert_serious('24RV', [[[1],[1,2,],[2,3],[3,4],[4]]])
        self.assert_serious('[1,2,3][3,4,5]^', [[4,5,1,2]])
        self.assert_serious('3R;2+^', [[4,5,1,2]])
        self.assert_serious('2[1,2,3]'+chr_cp437(0xCF),
                            [[[1, 2], [1, 3], [2, 3]]])
        self.assert_serious('23R'+chr_cp437(0xCF),
                            [[[1, 2], [1, 3], [2, 3]]])
        self.assert_serious('2[1,2,3]'+chr_cp437(0xD0),
                            [[[1, 2], [1, 3], [2, 1],
                             [2, 3], [3, 1], [3, 2]]])
        self.assert_serious('23R'+chr_cp437(0xD0),
                            [[[1, 2], [1, 3], [2, 1],
                             [2, 3], [3, 1], [3, 2]]])
        self.assert_serious('2[1,2,3]'+chr_cp437(0xF9),
                            [[[1, 1], [1, 2], [1, 3],
                             [2, 1], [2, 2], [2, 3],
                             [3, 1], [3, 2], [3, 3]]])
        self.assert_serious('23R'+chr_cp437(0xF9),
                            [[[1, 1], [1, 2], [1, 3],
                             [2, 1], [2, 2], [2, 3],
                             [3, 1], [3, 2], [3, 3]]])
        self.assert_serious('[1,2,3][1,2,3]'+chr_cp437(0xF9),
                            [[[1, 1], [1, 2], [1, 3],
                             [2, 1], [2, 2], [2, 3],
                             [3, 1], [3, 2], [3, 3]]])
        self.assert_serious('3R;'+chr_cp437(0xF9),
                            [[[1, 1], [1, 2], [1, 3],
                             [2, 1], [2, 2], [2, 3],
                             [3, 1], [3, 2], [3, 3]]])
        self.assert_serious('[1,2,3]♂D', [[0, 1, 2]])
        self.assert_serious('3R♂D', [[0, 1, 2]])
        self.assert_serious('[1,2,3];♀ⁿ', [[1, 4, 27]])
        self.assert_serious('3R;♀ⁿ', [[1, 4, 27]])
        self.assert_serious('[1,2,3]2♀>', [[1, 0, 0]])
        self.assert_serious('3R2♀>', [[1, 0, 0]])
        self.assert_serious('12♀>', [[1]])
        self.assert_serious('[1,2,3]/', [[3,1,2]])
        self.assert_serious('3R/', [[3,1,2]])
        self.assert_serious('[1,2,3]\\', [[2,3,1]])
        self.assert_serious('3R\\', [[2,3,1]])
        self.assert_serious('[1,2,3]d@q', [[1,2,3]])
        self.assert_serious('3Rd@q', [[1,2,3]])
        self.assert_serious('[1,2,3]p@o', [[1,2,3]])
        self.assert_serious('3Rp@o', [[1,2,3]])
        self.assert_serious('[1,2,3]i', [1,2,3])
        self.assert_serious('3Ri', [1,2,3])
        self.assert_serious('[1,2,3]R', [[3,2,1]])
        self.assert_serious('3RR', [[3,2,1]])
        self.assert_serious('1#', [[1]])
        self.assert_serious('"123"#', [['1','2','3']])
        self.assert_serious('[1,2,3]#', [[1,2,3]])
        self.assert_serious('3R#', [[1,2,3]])
        self.assert_serious('[1,2,3][0,1]'+chr_cp437(0xB0), [[2]])
        self.assert_serious('3R2r'+chr_cp437(0xB0), [[2]])
        self.assert_serious('[1,2,3]⌠2>⌡'+chr_cp437(0xB0), [[1]])
        self.assert_serious('3R⌠2>⌡'+chr_cp437(0xB0), [[1]])
        self.assert_serious('[1,2,3]N', [3])
        self.assert_serious('3RN', [3])
        self.assert_serious('[1,2,3]F', [1])
        self.assert_serious('3RF', [1])
        self.assert_serious('3[1,2,3,4]'+chr_cp437(0xD8), [[[1,2,3], [4]]])
        self.assert_serious('34R'+chr_cp437(0xB5), [[[1],[2],[3, 4]]])
        self.assert_serious('4#5'+chr_cp437(0xE0), [[4,4,4,4,4]])
        self.assert_serious('[4,5]5'+chr_cp437(0xE0), [[4, 5, 4, 5, 4, 5, 4, 5, 4, 5]])
        self.assert_serious('2R3'+chr_cp437(0xE0), [[1, 2, 1, 2, 1, 2]])
        self.assert_serious('3R'+chr_cp437(0xE6), [2.160246899469287])
        self.assert_serious('3Rd', [3, [1, 2]])
        self.assert_serious('3Rp', [1, [2, 3]])
        self.assert_serious('2406R'+chr_cp437(0xE8), [[1,3]])
        self.assert_serious('[0,4,2]6R'+chr_cp437(0xE8), [[1,3]])
        self.assert_serious('36R╡', [[[1, 2], [3, 4], [5, 6]]])
        self.assert_serious('3[1,2,3,4]╡', [[[1], [2], [3, 4]]])
        self.assert_serious('[[1,2],"ab",3]r', [[0,1,2]])
        self.assert_serious('[]r', [[]])
        self.assert_serious('"abc"r', [[0,1,2]])
        self.assert_serious('""r', [[]])
        self.assert_serious('⌠foo⌡r', [[0,1,2]])
        self.assert_serious('⌠⌡r', [[]])
        self.assert_serious('1[0,1,0,1,0,1,0]╢', [5])
        self.assert_serious('3R`+_', [6])
        self.assert_serious('3R`+┴', [[1, 3, 6]])

class BaseConversionTests(SeriousTest):
    def test_bases(self):
        self.assert_serious('2:5.5'+chr_cp437(0xAD), ["101.1"])
        self.assert_serious(':16:-26'+chr_cp437(0xAD), ["-1A"])
        self.assert_serious(':11'+chr_cp437(0xC3), ["1011"])
        self.assert_serious('"Foo"'+chr_cp437(0xC3), ["010001100110111101101111"])
        self.assert_serious(':3.07'+chr_cp437(0xC3), ['0100000000001000100011110101110000101000111101011100001010001111'])
        self.assert_serious(':256"{}"'.format(chr_cp437(0xA8)+chr_cp437(0xAD))+chr_cp437(0xA8), [0xA8*256+0xAD])
        self.assert_serious(':256:{}'.format(0xA8*256+0xAD)+chr_cp437(0xAD), [chr_cp437(0xA8)+chr_cp437(0xAD)])
        self.assert_serious('20k:16@'+chr_cp437(0xA8), [0x20])
        
class FunctionTests(SeriousTest):
    def test_function_methods(self):
        self.assert_serious('⌠foo⌡'+chr_cp437(0x9C), ['foo'])
        self.assert_serious('"foo"'+chr_cp437(0x9C), [SeriousFunction('foo')])
        self.assert_serious('5'+chr_cp437(0x9C), [5])
        self.assert_serious('⌠foo⌡l', [3])
        self.assert_serious('⌠bar⌡⌠foo⌡+', [SeriousFunction('foobar')])
        self.assert_serious('⌠foo⌡3*', [SeriousFunction('foofoofoo')])
        self.assert_serious('["oo"]⌠f%s⌡%', [SeriousFunction('foo')])
        self.assert_serious('⌠foo⌡"foo"=', [1])
        self.assert_serious('⌠foo⌡⌠bar⌡=', [0])
        self.assert_serious('⌠foo⌡3=', [3, SeriousFunction('foo')])
        self.assert_serious('[1,2,3]⌠++⌡R', [[6]])
        self.assert_serious('3`1n', [1,1,1])
        self.assert_serious('5⌠2@%Y⌡'+chr_cp437(0xD6), [[0,2,4,6,8]])
        self.assert_serious('[1,2,3,4,5]`pc', [3])
        self.assert_serious('[2,4,6,8]⌠5>⌡c', [2])
        
    def test_combinators(self):
        self.assert_serious('3⌠1kMD⌡Y', [0])
        
class RandomTests(SeriousTest):
    def test_random(self):
        random.seed(0)
        self.assert_serious('2v52BG52V6J"abcd"J"abcd"'+chr_cp437(0xC8), ['badc', 'c', 1, 3.0831724219508216, 0.09158478740507359, 2])


class TestProbablyPrime(unittest.TestCase):
    def test_simple(self):
        self.assertTrue(probably_prime(13))

    def test_first_1000(self):
        for num in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                    103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                    449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                    587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                    853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                    991, 997]:
            self.assertTrue(probably_prime(num))
    def test_large(self):
        large_primes = [19823931826121, 21718972014737, 2866953310097]
        for num in large_primes:
            self.assertTrue(probably_prime(num))
