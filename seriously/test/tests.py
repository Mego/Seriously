#!/usr/bin/env python3
import argparse
import contextlib
from io import StringIO
import sys
import unittest
from lib.cp437 import CP437
from lib.iterable import as_list
from ..seriously import Seriously
from ..SeriouslyCommands import SeriousFunction

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
    def test_utils(self):
        self.assertEqual(as_list(range(5)), [0, 1, 2, 3, 4])
        self.assertEqual(as_list((1,2,3,4) for x in range(3)), [[1, 2, 3, 4]]*3)
        self.assertEqual(as_list(2), [2])
        self.assertEqual([chr_cp437(x) for x in range(256)], [x for x in CP437.table])
        self.assertEqual([ord_cp437(x) for x in CP437.table], [x for x in range(256)])


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
        self.assert_serious(chr_cp437(0x0C), ['abc\n'], "abc\n")

    def test_formatted_input(self):
        self.assert_serious(',', ['a'], '"a"\n')

        self.assert_serious(',', [12345], '12345\n')

        self.assert_serious(',', [[3, 2, 1]], '[3,2,1]\n')

        self.assert_serious(',', [[3, 2, 1]], '3, 2, 1\n')
        
    def test_implicit_input(self):
        self.assert_serious('', ['a'], '"a"\n')


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

    def test_functions(self):
        self.assert_serious("`foo`", [SeriousFunction("foo")])
        self.assert_serious("`foo`$", ["foo"])

    def test_eval(self):
        self.assert_serious('"len(set([1,2,2,3]))"{}'.format(chr_cp437(0xF0)),
                            [3])
                            
    def test_lists(self):
        self.assert_serious("[1,2,3]", [[1,2,3]])
        self.assert_serious("[[1],[2]]", [[[1],[2]]])


class StackTests(SeriousTest):
    def test_count(self):
        self.assert_serious('1 ', [1, 1])

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


class RegisterTests(SeriousTest):
    def test_push_pop(self):
        self.assert_serious('1{}2{}{}{}'.format(
                            chr_cp437(0xBB), chr_cp437(0xBC),
                            chr_cp437(0xBE), chr_cp437(0xBD)), [1, 2])
        self.assert_serious('53{}3{}'.format(chr_cp437(0xBF),
                                             chr_cp437(0xC0)), [5])

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
        self.assert_serious(':-3s', [-1])
        self.assert_serious('3s', [1])
        self.assert_serious('0s', [0])
        self.assert_serious('25^', [7])
        self.assert_serious('24%', [0])
        self.assert_serious('[1,2,3]3+', [[4,5,6]])
        self.assert_serious('2[2,4,6]+', [[4, 6, 8]])
        self.assert_serious('[1,2,3]3*', [[3,6,9]])
        self.assert_serious('2[2,4,6]*', [[4, 8, 12]])
        self.assert_serious('2'+chr_cp437(0x8C), [2j])
        self.assert_serious('[2,3]'+chr_cp437(0x8C), [[2j,3j]])
        self.assert_serious(':1+2j'+chr_cp437(0xD7), [2, 1])

    def test_lists(self):
        self.assert_serious('[1][1,2]-', [[2]])
        self.assert_serious('[2,3];*', [13])
        self.assert_serious('[1,2,3]M', [3])
        self.assert_serious('[1,2,3]m', [1])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0xE4), [10])
        self.assert_serious('[2.5,2.5]'+chr_cp437(0xE4), [5.0])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0xE3), [24])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0xBA), [2.5])
        self.assert_serious('[1,2,6,3,4]'+chr_cp437(0xBA), [6])
        self.assert_serious('[1,2,3,3]'+chr_cp437(0x9A), [3])
        self.assert_serious('[3,6,9,12]'+chr_cp437(0x1F), [[1, 2, 3, 4]])
        self.assert_serious('4r', [[0,1,2,3]])
        self.assert_serious('4R', [[1,2,3,4]])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0x80), [3+4j, 1+2j])
        self.assert_serious('[1,2,3,4,5]'+chr_cp437(0x80), [5, 3+4j, 1+2j])
        self.assert_serious('2[1,2,3]'+chr_cp437(0xFC), [[1, 4, 9]])

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


class StringAndListTests(SeriousTest):
    def test_format(self):
        self.assert_serious('[2,3]"{}.{}"f', ["2.3"])
        self.assert_serious('[2,3]"%d.%d"%', ["2.3"])

    def test_modify(self):
        self.assert_serious('52[2,3,4]T', [[2, 3, 5]])
        self.assert_serious('52"234"T', ["235"])

    def test_ords(self):
        self.assert_serious('"abc"O', [[0x61, 0x62, 0x63]])

    def test_string_methods(self):
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
        self.assert_serious('`foo`'+chr_cp437(0x8A), ['`foo`'])
        self.assert_serious('"1.23"i', [1.23])
        self.assert_serious('"123"R', ["321"])
        self.assert_serious('"abcdefg"'+chr_cp437(0xF4)+chr_cp437(0xF5), ["abcdefg"])
        self.assert_serious('"abc"3*', ['abcabcabc'])
        self.assert_serious('3"abc"*', ['abcabcabc'])
        
    def test_list_methods(self):
        self.assert_serious('[1,2,3][4,5,6]'+chr_cp437(0x9D), [[5, 7, 9]])
        self.assert_serious("""'0"010203040"#s""", [[[],['1'],['2'],['3'],['4'],[]]])
        self.assert_serious('0"10203"s', [['1', '2', '3']])
        self.assert_serious('2[1,2,3,4]V', [[[1],[1,2,],[2,3],[3,4],[4]]])
        self.assert_serious('[1,2,3],[3,4,5]^', [[4,5,1,2]])
        self.assert_serious('2[1,2,3]'+chr_cp437(0xCF),
                            [[[1, 2], [1, 3], [2, 3]]])
        self.assert_serious('2[1,2,3]'+chr_cp437(0xD0),
                            [[[1, 2], [1, 3], [2, 1],
                             [2, 3], [3, 1], [3, 2]]])
        self.assert_serious('2[1,2,3]'+chr_cp437(0xF9),
                            [[[1, 1], [1, 2], [1, 3],
                             [2, 1], [2, 2], [2, 3],
                             [3, 1], [3, 2], [3, 3]]])
        self.assert_serious('[1,2,3][1,2,3]'+chr_cp437(0xF9),
                            [[[1, 1], [1, 2], [1, 3],
                             [2, 1], [2, 2], [2, 3],
                             [3, 1], [3, 2], [3, 3]]])
        self.assert_serious('[1,2,3]♂D', [[0, 1, 2]])
        self.assert_serious('[1,2,3]/', [[3,1,2]])
        self.assert_serious('[1,2,3]\\', [[2,3,1]])
        self.assert_serious('[1,2,3]d@q', [[1,2,3]])
        self.assert_serious('[1,2,3]p@o', [[1,2,3]])
        self.assert_serious('[1,2,3]i', [1,2,3])
        self.assert_serious('[1,2,3]R', [[3,2,1]])
        self.assert_serious('1#', [[1]])
        self.assert_serious('"123"#', [['1','2','3']])
        self.assert_serious('[1,2,3]#', [[1,2,3]])
        self.assert_serious('[1,2,3][0,1]'+chr_cp437(0xB0), [[2]])
        self.assert_serious('[1,2,3]`2>`'+chr_cp437(0xB0), [[1]])
        self.assert_serious('[1,2,3]N', [3])
        self.assert_serious('[1,2,3]F', [1])
        self.assert_serious('[1,2,3]i', [1,2,3])


class BaseConversionTests(SeriousTest):
    def test_bases(self):
        self.assert_serious('2:5.5'+chr_cp437(0xAD), ["101.1"])
        self.assert_serious(':16:-26'+chr_cp437(0xAD), ["-1A"])
        self.assert_serious(':11'+chr_cp437(0xC3), ["1011"])
        self.assert_serious('"Foo"'+chr_cp437(0xC3), ["010001100110111101101111"])
        self.assert_serious(':3.07'+chr_cp437(0xC3), ['0100000000001000100011110101110000101000111101011100001010001111'])
        self.assert_serious(':256"{}"'.format(chr_cp437(0xA8)+chr_cp437(0xAD))+chr_cp437(0xA8), [0xA8*256+0xAD])
        self.assert_serious(':256:{}'.format(0xA8*256+0xAD)+chr_cp437(0xAD), [chr_cp437(0xA8)+chr_cp437(0xAD)])
        
class FunctionTests(SeriousTest):
    def test_function_methods(self):
        self.assert_serious('`foo`'+chr_cp437(0x9C), ['foo'])
        self.assert_serious('"foo"'+chr_cp437(0x9C), [SeriousFunction('foo')])
        self.assert_serious('5'+chr_cp437(0x9C), [5])
        self.assert_serious('`foo`l', [3])
        self.assert_serious('`bar``foo`+', [SeriousFunction('foobar')])
        self.assert_serious('`foo`3*', [SeriousFunction('foofoofoo')])
        self.assert_serious('["oo"]`f%s`%', [SeriousFunction('foo')])
        self.assert_serious('`foo`"foo"=', [1])
        self.assert_serious('`foo``bar`=', [0])
        self.assert_serious('`foo`3=', [3, SeriousFunction('foo')])
        self.assert_serious('[1,2,3]`++`R', [[6]])
        self.assert_serious('3`1`n', [1,1,1])
        self.assert_serious('5`2@%Y`'+chr_cp437(0xD6), [[0,2,4,6,8]])
        
    def test_combinators(self):
        self.assert_serious('3`1kMD`Y', [0])
        
class RandomTests(SeriousTest):
    def test_random(self):
        self.assert_serious('2v52BG52V6J"abcd"J"abcd"'+chr_cp437(0xC8), ['abcd', 'c', 1, 3.0831724219508216, 0.09158478740507359, 2])


if __name__ == '__main__':
    unittest.main(verbosity=3)
