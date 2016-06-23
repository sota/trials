#!/usr/bin/env python

import re

class Token(object):
    def __init__(self, line, pos, kind, value):
        self.line = line
        self.pos = pos
        self.kind = kind if kind is not True else value
        self.value = value

    def __str__(self):
        return '[line=%d pos=%d kind=%s value=%s]' % (
            self.line,
            self.pos,
            self.kind,
            self.value)

    def __repr__(self):
        fmt = 'Token(%s, %s, %s, %s)'
        return fmt % (
            self.line,
            self.pos,
            self.kind,
            self.value)

#    def is_kind(self, *kinds):
#        return any(map(lambda kind: self.kind == kind, kinds))

    def is_kind(self, *kinds):
        return self.kind in kinds

    def is_id(self, *ids):
        if self.kind == 'ID':
            return self.value in ids
        return False


