#!/usr/bin/env python

import os

from pprint import pprint

from v1.environment import *
from v1.expressions import *

class Parser(object):
    def __init__(self, lexer, verbose):
        assert lexer
        self.lexer = lexer
        self.verbose = verbose

    def Parse(self, source):
        exitcode = 0
        env = Env
        if os.path.isfile(source):
            source = open(source).read()
        else:
            source = "(print " + source + ")"
        try:
            code = self.Read(source)
            if self.verbose:
                print 'code =', code
            self.Eval(code, env)
        except Exception as ex:
            raise
        return exitcode

    def Repl(self):
        exitcode = 0
        env = Env
        farewell = "so, ta-ta for now!"
        print REPL_USAGE
        prompt = "sota> "
        while True:
            os.write(1, prompt)
            source = None
            try:
                source = get_input()
                if source == '\n':
                    continue
                code = self.Read(source)
                exp = self.Eval(code, env)
                if exp is None:
                    print farewell
                    break
                self.Print(exp)
            except KeyboardInterrupt:
                break
            except EOFError:
                print farewell
                break
        return exitcode

    def Read(self, source=None):
        if source:
            self.lexer.Scan(source)
        token = self.lexer.Consume()
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
        token, _, _ = self.lexer.Lookahead1()
        assert token
        if token.is_kind(')'):
            self.lexer.Consume()
            return nil
        car = self.Read()
        token, _, _ = self.lexer.Lookahead1()
        assert token
        if token.is_kind('.'):
            self.lexer.Consume()
            cdr = self.Read()
            if not self.lexer.Consume(')'):
                raise Exception
        else:
            cdr = self.ReadPair()
        return SastPair(car, cdr)

    def ReadBlock(self):
        token, _, _ = self.lexer.Lookahead1()
        assert token
        if token.is_kind('}'):
            self.lexer.Consume()
            return nil
        car = self.Read()
        token, _, _ = self.lexer.Lookahead1()
        assert token
        cdr = self.ReadBlock()
        return SastPair(car, cdr)

    def Eval(self, exp, env):
        pass
