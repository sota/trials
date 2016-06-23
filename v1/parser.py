#!/usr/bin/env python

import os

from pprint import pprint

from v1.environment import *
from v1.expressions import *

class Parser(object):
    def __init__(self, verbose):
        self.index = 0
        self.verbose = verbose

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
    def Parse(self, tokens):
        assert tokens
        self.tokens = tokens
        exitcode = 0
        env = Env
        try:
            code = self.Read()
            if self.verbose:
                print 'code =', code
            self.Eval(code, env)
        except Exception as ex:
            raise
        return exitcode

    def Read(self):
        token = self.Consume()
        if token.is_kind('ID'):
            if token.is_id('true'):
                return SastBool.true
            elif token.is_id('false'):
                return SastBool.false
            elif token.is_kind('='):
                return Assign
            elif token.is_id("'"):
                return SastSymbol('quote')
            return SastSymbol(token.value)
        elif token.is_kind('STR'):
            return SastString(token.value)
        elif token.is_kind('NUM'):
            return SastNumber(int(token.value))
        elif token.is_kind('('):
            return self.ReadPair()
        elif token.is_kind('{'):
            stmts = self.ReadBlock()
            return SastBlock(stmts)
        return SastUndefined()

    def ReadPair(self):
        token, _, _ = self.Lookahead1()
        assert token
        if token.is_kind(')'):
            self.Consume()
            return nil
        car = self.Read()
        token, _, _ = self.Lookahead1()
        assert token
        if token.is_kind('.'):
            self.Consume()
            cdr = self.Read()
            if not self.Consume(')'):
                raise Exception
        else:
            cdr = self.ReadPair()
        return SastPair(car, cdr)

    def ReadBlock(self):
        token, _, _ = self.Lookahead1()
        assert token
        if token.is_kind('}'):
            self.Consume()
            return nil
        car = self.Read()
        token, _, _ = self.Lookahead1()
        assert token
        cdr = self.ReadBlock()
        return SastPair(car, cdr)

    def Eval(self, exp, env):
        pass
