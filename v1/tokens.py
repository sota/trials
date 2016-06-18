#!/usr/bin/env python

import re

def regex(s):
    return re.compile(s)

TOKENS =[
    (regex('[ \n\t]+'),                                             False),
    (regex('[=\+\-\.\^\$\*\(\)\[\]\{\}\|\/\\\\]{1,2}'),             True),
    (regex('#[^\n]*'),                                              'CMT'),
    (regex('[0-9]+'),                                               'NUM'),
    (regex('"[^"]*"'),                                              'STR'),
    (regex('([A-Za-z0-9_]*[@\&\+\-\|]*)*[A-Za-z0-9_]+[\?\!]?'),     'ID'),
]

class Token(object):
    def __init__(self, kind, value, line, pos):
        self.kind = kind if kind is not True else value
        self.value = value
        self.line = line
        self.pos = pos

    def __str__(self):
        return '[kind=%s value=%s line=%d pos=%d]' % (
            self.kind,
            self.value,
            self.line,
            self.pos)

    def __repr__(self):
        return 'Token(%s, %s, %s, %s)' % (
            self.kind,
            self.value,
            self.line,
            self.pos)

    def is_kind(self, *kinds):
        return any(map(lambda kind: self.kind == kind, kinds))


