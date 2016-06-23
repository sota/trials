#!/usr/bin/env python

import os
import re
import imp
import sys
sys.dont_write_bytecode = True

from pprint import pprint
from argparse import ArgumentParser

VERSION = 'v1'
lexer = imp.load_source('lexer', VERSION+'/lexer.py')
parser = imp.load_source('parser', VERSION+'/parser.py')
patterns = imp.load_source('patterns', VERSION+'/patterns.py')
vm = imp.load_source('vm', VERSION+'/vm.py')

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

    lexer = lexer.Lexer(patterns.PATTERNS, ns.verbose)
    parser = parser.Parser(ns.verbose)

    if not ns.source:
        exitcode = repl(lexer, parser)

    if os.path.isfile(ns.source):
        source = open(ns.source).read()
    else:
        source = '(print %s)' % ns.source

    tokens = lexer.Scan(source)
    exitcode = parser.Parse(tokens)

    sys.exit(exitcode)

