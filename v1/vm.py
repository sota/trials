#!/usr/bin/env python

from pprint import pprint

def execute(bytecodes, verbose):
    exitcode = 0
    if verbose:
        pprint({'exitcode':exitcode})
    return exitcode
