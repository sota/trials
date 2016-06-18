#!/usr/bin/env python

import re

CMT, NUM, STR, ID = 'CMT', 'NUM', 'STR', 'ID'

TOKENS =[
    (re.compile('[ \n\t]+'),                                            False),
    (re.compile('[:\(\)\[\]\{\}]'),                                     True),
    (re.compile('[;=<>\+\-\.\^\$\*\|\/\\\\]{1,3}'),                     True),
    (re.compile('#[^\n]*'),                                             CMT),
    (re.compile('[0-9]+'),                                              NUM),
    (re.compile('"[^"]*"'),                                             STR),
    (re.compile('([A-Za-z0-9_]*[@\&\+\-\|]*)*[A-Za-z0-9_]+[\?\!]?'),    ID),
]

class Token(object):
    def __init__(self, kind, line, pos, value):
        self.kind = kind if kind is not True else value
        self.line = line
        self.pos = pos
        self.value = value

    def __str__(self):
        return '[kind=%s line=%d pos=%d value="%s"]' % (
            self.kind,
            self.line,
            self.pos,
            self.value)

    def __repr__(self):
        fmt = 'Token(%s, %s, %s, "%s")'
        return fmt % (
            self.kind,
            self.line,
            self.pos,
            self.value)

    def is_kind(self, *kinds):
        return any(map(lambda kind: self.kind == kind, kinds))


