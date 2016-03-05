#!/usr/bin/env python3
import multiprocessing
import subprocess
import sys
from lib.cp437 import CP437

ord_cp437 = CP437.ord
chr_cp437 = CP437.chr


class SeriousError(SystemExit):
    def __init__(self, *args):
        super().__init__()
        self.args = args

    def __str__(self):
        return repr(self.args)


def serious_call(args):
    code, result, cinput, errors = args
    p = subprocess.Popen(['python3', 'seriously.py', '-c', code],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         universal_newlines=True)
    out, err = p.communicate(cinput)
    return code, cinput, out, err, result, errors


run_queue = []


def serious_check(code, result, cinput='', errors=True):
    global run_queue
    run_queue.append((code, result, cinput, errors))


def run_tests():
    global run_queue
    with multiprocessing.Pool() as pool:
        r = pool.imap_unordered(serious_call, run_queue)
        for res in r:
            code, cinput, output, error, result, errors = res
            res2 = {'code': code, 'input': cinput, 'output': output,
                    'error': error, 'result': result, 'errors': errors}
            if (errors and error) or (output != result):
                print("Bad: {}".format(res2))
                return False
    return True

if __name__ == '__main__':
    # I/O tests
    serious_check(chr_cp437(0x09),'a\n','a')
    serious_check(r',','a\n','"a"')
    serious_check(r',','abc\n','"abc"')
    serious_check(r',','12345\n','12345')
    serious_check(r',','[3, 2, 1]\n','[3,2,1]')
    serious_check(chr_cp437(0x0C), "abc\n", 'abc')

    # Literals tests
    serious_check(r'"a','a\n')
    serious_check(r"'a",'a\n')
    for i in range(10):
        serious_check(r'%d'%i,'%d\n'%i)
    serious_check(r':12345','12345\n')
    serious_check(r':12345D', '12344\n')
    serious_check(r':1.25','1.25\n')
    serious_check(r':1+2j','(1+2j)\n')
    serious_check(r'[1,2+0j,"fizz",4.0,"buzz"]',"[1, (2+0j), 'fizz', 4.0, 'buzz']\n")
    serious_check(r'`foo`','foo\n')
    serious_check(r'"len(set([1,2,2,3]))"{}'.format(chr_cp437(0xF0)), '3\n')

    # Meta stack tests
    serious_check(r'1 ','1\n1\n')
    serious_check(r'123(','1\n3\n2\n')
    serious_check(r'123)','2\n1\n3\n')
    serious_check(r'123@','2\n3\n1\n')
    serious_check(r'Q','Q\n')
    serious_check(r'5W;.D','5\n4\n3\n2\n1\n0\n')
    serious_check(r'123a','1\n2\n3\n')
    serious_check(r'123'+chr_cp437(0x7F),'')
    serious_check(r'123'+chr_cp437(0xB3),'3\n2\n1\n'*2)
    serious_check(r'123'+chr_cp437(0xC5),'3\n3\n2\n2\n1\n1\n')
    serious_check(r'12'+chr_cp437(0xC6),'1\n1\n')
    serious_check(r'123'+chr_cp437(0xFE),'3 2 1\n3\n2\n1\n')

    # Registers tests
    serious_check(r'1%s2%s%s%s'%(chr_cp437(0xBB),chr_cp437(0xBC),chr_cp437(0xBE),chr_cp437(0xBD)),'1\n2\n')
    serious_check(r'53%s3%s'%(chr_cp437(0xBF),chr_cp437(0xC0)),'5\n')

    # Math tests
    serious_check(r'[1][1,2]-','[2]\n')
    serious_check(r'[1,2,3]M','3\n')
    serious_check(r'[1,2,3]m','1\n')
    serious_check(r'[2,3][2,3]*','13\n')
    serious_check(r'[4][1,2,"3"]q'+chr_cp437(0x8D), '[1, 2]\n')
    serious_check(r'[4][1,2,"3"]q'+chr_cp437(0x92), "['3']\n")
    serious_check(r'[4][1,2,"3"]q'+chr_cp437(0xA5), '[[4]]\n')
    serious_check(r'2'+chr_cp437(0xB9), '[1, 2, 1]\n')
    serious_check(r':16'+chr_cp437(0xDF), "0123456789ABCDEF\n")
    serious_check(r'[1,2,3,4]'+chr_cp437(0xE4), "10\n")
    serious_check(r'[1,2,3,4]'+chr_cp437(0xE3), "24\n")
    serious_check(r'[1,2,3,4]'+chr_cp437(0xBA), "2.5\n")
    serious_check(r'[1,2,3,3]'+chr_cp437(0x9A), "3\n")
    serious_check(r'[2.5, 2.5]'+chr_cp437(0xE4), "5.0\n")
    serious_check(r'8f', "6\n")
    serious_check(r'1T'+chr_cp437(0x85), "1.0\n")

    # String tests
    serious_check(r'[2,3]"{}.{}"f', "2.3\n")
    serious_check(r'52[2,3,4]T', "[2, 3, 5]\n")
    serious_check(r'52"234"T', "235\n")
    serious_check(r'"%s"O'%(chr_cp437(0x57)+chr_cp437(0x58)+chr_cp437(0x59)), "[%s, %s, %s]\n"%(0x57,0x58,0x59))
    serious_check(r'["%s"]O'%(chr_cp437(0x57)+chr_cp437(0x58)+chr_cp437(0x59)), "[%s, %s, %s]\n"%(0x57,0x58,0x59))

    # Base tests
    serious_check(r'2:5.5%s'%(chr_cp437(0xAD)), "101.1\n")

    # List tests
    serious_check(r'2[1,2,3]'+chr_cp437(0xCF), "[[1, 2], [1, 3], [2, 3]]\n")
    serious_check(r'2[1,2,3]'+chr_cp437(0xD0), "[[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]\n")
    serious_check(r'2[1,2,3]'+chr_cp437(0xF9), "[[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]\n")
    serious_check(r'[1,2,3][1,2,3]'+chr_cp437(0xF9), "[[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]\n")

    # More to come...

    assert run_tests()
