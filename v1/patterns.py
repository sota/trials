import re

CMT, NUM, STR, ID = 'CMT', 'NUM', 'STR', 'ID'

PATTERNS =[
    (re.compile('[ \n\t]+'),                                            False),
    (re.compile('[:\(\)\[\]\{\}]'),                                     True),
    (re.compile('[;=<>\+\-\.\^\$\*\|\/\\\\]{1,3}'),                     True),
    (re.compile('#[^\n]*'),                                             CMT),
    (re.compile('[0-9]+'),                                              NUM),
    (re.compile('"[^"]*"'),                                             STR),
    (re.compile('([A-Za-z0-9_]*[@\&\+\-\|]*)*[A-Za-z0-9_]+[\?\!]?'),    ID),
]

