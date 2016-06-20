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
        self.source = None
        self.tokens = []
        self.index = 0
        assert patterns
        self.patterns = patterns
        self.verbose = verbose

    def Scan(self, source):
        self.index = index = 0
        self.source = source
        del self.tokens[:]
        while index < len(source):
            match = None
            previous = source[0:index]
            for regex, kind in self.patterns:
                match = regex.match(source, index)
                if match:
                    value = match.group(0)
                    if kind:
                        self.tokens += [Token(kind, line(previous), pos(previous), value)]
                    break
            if not match:
                sys.stderr.write('illegal character: %s\n' % source[index])
                sys.exit(1)
            else:
                index = match.end(0)
        if self.verbose:
            pprint({'tokens':self.tokens})
        return self.tokens

    def Lookahead(self, distance, expect=None, skips=False):
        index = self.index
        token = None
        while distance:
            if index < len(self.tokens):
                token = self.tokens[index]
            else:
                break
            if token:
                #if skips: # or not token.skip:
                distance -= 1
            index += 1
        distance = index - self.index
        return token, distance, (token.kind == expect) if token and expect else expect

    def Lookahead1(self, expect=None):
        return self.Lookahead(1, expect)

    def Lookahead2(self, expect=None):
        return self.Lookahead(2, expect)

    def Consume(self, *expects):
        token, distance, _ = self.Lookahead1()
        if not token:
            raise Exception
        if len(expects):
            for expect in expects:
                if expect == token.name:
                    self.index += distance
                    return token
            return None
        self.index += distance
        return token
