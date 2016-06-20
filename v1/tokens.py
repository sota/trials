#!/usr/bin/env python

import re

class Token(object):
    def __init__(self, kind, line, pos, value):
        self.kind = kind if kind is not True else value
        self.line = line
        self.pos = pos
        self.value = value

    def __str__(self):
        return '[kind=%s line=%d pos=%d value=%s]' % (
            self.kind,
            self.line,
            self.pos,
            self.value)

    def __repr__(self):
        fmt = 'Token(%s, %s, %s, %s)'
        return fmt % (
            self.kind,
            self.line,
            self.pos,
            self.value)

#    def is_kind(self, *kinds):
#        return any(map(lambda kind: self.kind == kind, kinds))

    def is_kind(self, *kinds):
        return self.kind in kinds

    def is_id(self, *ids):
        if self.kind == 'ID':
            return self.value in ids
        return False


