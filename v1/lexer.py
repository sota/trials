#!/usr/bin/env python

import sys

from pprint import pprint
from v1.tokens import Token, TOKENS

def escape(s):
    return s.replace('\n', '\\n').replace('\t', '\\t')

def line(s):
    return s.count('\n') + 1

def pos(s):
    return len(s) - s.rfind('\n')

def scan(content, verbose):
    tokens = []
    index = 0
    while index < len(content):
        match = None
        previous = content[0:index]
        for regex, kind in TOKENS:
            match = regex.match(content, index)
            if match:
                value = match.group(0)
                if kind:
                    tokens += [Token(kind, value, line(previous), pos(previous))]
                break
        if not match:
            sys.stderr.write('illegal character: %s\n' % content[index])
            sys.exit(1)
        else:
            index = match.end(0)
    if verbose:
        pprint({'tokens':tokens})
    return tokens
