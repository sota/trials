#!/usr/bin/env python

import sys

from pprint import pprint
from v1.tokens import Token

def escape(s):
    return s.replace('\n', '\\n').replace('\t', '\\t')

def line(s):
    return s.count('\n') + 1

def pos(s):
    return len(s) - s.rfind('\n')

class Lexer(object):

    def __init__(self, patterns, verbose):
        assert patterns
        self.patterns = patterns
        self.verbose = verbose

    def Scan(self, source):
        assert source
        self.source = source
        self.index = index = 0
        tokens = []
        while index < len(self.source):
            match = None
            previous = self.source[0:index]
            for regex, kind in self.patterns:
                match = regex.match(self.source, index)
                if match:
                    value = match.group(0)
                    if kind:
                        tokens += [Token(line(previous), pos(previous), kind, value)]
                    break
            if not match:
                sys.stderr.write('illegal character: %s\n' % self.source[index])
                sys.exit(1)
            else:
                index = match.end(0)
        if self.verbose:
            pprint({'tokens':tokens})
        return tokens

