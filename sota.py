#!/usr/bin/env python

import os
import re
import imp
import sys
sys.dont_write_bytecode = True

from pprint import pprint
from argparse import ArgumentParser

VERSION = 'v1'
sys.path.insert(0, VERSION)
from lexer import Lexer
from parser import Parser
from virtualmachine import VirtualMachine
from patterns import PATTERNS
from environment import Env

REPL_USAGE = '''
Usage
'''

def get_input():
    raise NotImplementedError

#FIXME: what to do with this?
def repl(lexer, parser):
    exitcode = 0
    env = Env
    farewell = "so, ta-ta for now!"
    print REPL_USAGE
    prompt = "sota> "
    while True:
        os.write(1, prompt)
        source = None
        try:
            source = get_input()
            if source == '\n':
                continue
            tokens = lexer.Scan(source)
            bytecodes = parser.Parse(tokens)
            #code = self.Read(source)
            #exp = self.Eval(code, env)
            if exp is None:
                print farewell
                break
            #self.Print(exp)
        except KeyboardInterrupt:
            break
        except EOFError:
            print farewell
            break
    return exitcode


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument(
        '-V', '--version',
        action='version',
        version=VERSION,
        help='print the version and exit')
    ap.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='print verbosely')
    ap.add_argument(
        'source',
        default=None,
        nargs='?',
        help='text | file')

    ns = ap.parse_args()
    print ns

    lexer = Lexer(PATTERNS, ns.verbose)
    parser = Parser(ns.verbose)
    vm = VirtualMachine()

    if not ns.source:
        exitcode = repl(lexer, parser)

    if os.path.isfile(ns.source):
        source = open(ns.source).read()
    else:
        source = '(print %s)' % ns.source

    tokens = lexer.Scan(source)
    opcodes = parser.Parse(tokens)
    exitcode =vm.Execute(opcodes)

    sys.exit(exitcode)

