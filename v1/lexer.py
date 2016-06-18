#!/usr/bin/env python

import sys
from v1.tokens import Token, TOKENS

def scan(content, verbose):
    tokens = []
    pos = 0
    while pos < len(content):
        match = None
        for regex, kind in TOKENS:
            match = regex.match(content, pos)
            if match:
                name = match.group(0)
                if kind:
                    token = Token(name, kind, 0, 0, False)
                    tokens += [token]
                break
        if not match:
            sys.stderr.write('illegal character: %s\n' % content[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    if verbose:
        print tokens
    return tokens
