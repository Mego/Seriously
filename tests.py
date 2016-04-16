#!/usr/bin/env python3
import contextlib
from io import StringIO
import sys
import unittest
from lib.cp437 import CP437
from seriously import Seriously
from SeriouslyCommands import SeriousFunction

ord_cp437 = CP437.ord
chr_cp437 = CP437.chr


class SeriousTest(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        if not hasattr(self, 'subTest'):
            self.subTest = self.dummy_manager

    @contextlib.contextmanager
    def dummy_manager(*args, **kwargs):
        yield

    def setUp(self):
        self.srs = Seriously()

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

    def test_eval(self):
        self.assert_serious('"len(set([1,2,2,3]))"{}'.format(chr_cp437(0xF0)),
                            [3])


class StackTests(SeriousTest):
    def test_count(self):
        self.assert_serious('1 ', [1, 1])

    def test_rotations(self):
        self.assert_serious('123(', [1, 3, 2])
        self.assert_serious('123)', [2, 1, 3])
        self.assert_serious('123@', [2, 3, 1])

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

    def test_lists(self):
        self.assert_serious('[1][1,2]-', [[2]])
        self.assert_serious('[2,3];*', [13])
        self.assert_serious('[1,2,3]M', [3])
        self.assert_serious('[1,2,3]m', [1])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0xE4), [10])
        self.assert_serious('[2.5,2.5]'+chr_cp437(0xE4), [5.0])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0xE3), [24])
        self.assert_serious('[1,2,3,4]'+chr_cp437(0xBA), [2.5])
        self.assert_serious('[1,2,3,3]'+chr_cp437(0x9A), [3])

    def test_filters(self):
        self.assert_serious("[4]12'3k"+chr_cp437(0x8D), [[1, 2]])
        self.assert_serious("[4]12'3k"+chr_cp437(0x92), [['3']])
        self.assert_serious("[4]12'3k"+chr_cp437(0xA5), [[[4]]])

    def test_sequences(self):
        self.assert_serious('4p', [0])
        self.assert_serious(':23p', [1])
        self.assert_serious('3P', [7])
        self.assert_serious('8f', [6])
        self.assert_serious(':16'+chr_cp437(0xDF), ['0123456789ABCDEF'])
        self.assert_serious('2'+chr_cp437(0xB9), [[1, 2, 1]])

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
        self.assert_serious('"abcd"3N', ["abc"])
        self.assert_serious('"abcd"30-N', ["bcd"])


class BaseConversionTests(SeriousTest):
    def test_bases(self):
        self.assert_serious('2:5.5'+chr_cp437(0xAD), ["101.1"])


class ListTests(SeriousTest):
    def test_lists(self):
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

if __name__ == '__main__':
    unittest.main(verbosity=3)
