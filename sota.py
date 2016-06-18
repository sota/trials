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
vm = imp.load_source('vm', VERSION+'/vm.py')

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
        help='text | file')

    ns = ap.parse_args()
    print ns

    content = ns.source
    if os.path.isfile(ns.source):
        content = open(ns.source).read()
    tokens = lexer.scan(content, ns.verbose)
    bytecodes = parser.parse(tokens, ns.verbose)
    exitcode = vm.execute(bytecodes, ns.verbose)
    sys.exit(exitcode)

