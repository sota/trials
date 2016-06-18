#!/usr/bin/env python

import re

def regex(s):
    return re.compile(s)

TOKENS =[
    (regex('[ \n\t]+'),                     False),
    (regex('[\.\^\$\*\+\(\)\[\]\{\}\|]'),   True),
    (regex('#[^\n]*'),                      'COMMENT'),
    (regex('[0-9]+'),                       'NUMBER'),
    (regex('"[A-Za-z0-9]*"'),               'STRING'),
    (regex('[A-Za-z][A-Za-z0-9_]*'),        'SYMBOL'),
]

class Token(object):
    def __init__(self, name, value, line, pos, skip):
        self.name = name
        self.value = value
        self.line = line
        self.pos = pos
        self.skip = skip

    def __str__(self):
        return '[name=%s value=%s line=%d pos=%d skip=%s]' % (
            self.name,
            self.value,
            self.line,
            self.pos,
            self.skip)

    def __repr__(self):
        return 'Token(%s, %s, %s, %s, %s)' % (
            self.name,
            self.value,
            self.line,
            self.pos,
            self.skip)

    def is_name(self, *names):
        return any(map(lambda name: self.name == name, names))


