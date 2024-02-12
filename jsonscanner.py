import re
from collections import namedtuple


SKIP_RE = re.compile(r'(( |\t)|\#.*)+')
INT_RE = re.compile(r'\d+')
LEFT_SQUARE=re.compile(r'\[')
RIGHT_SQUARE=re.compile(r'\]')
COLON=re.compile(r':')
COMMA=re.compile(r',')
LEFT_CURLY=re.compile(r'\{')
RIGHT_CURLY=re.compile(    r'\}': )
LEFT_PERCENT_CURLY=re.compile(    r'%\{')
ARROW=re.compile(    r'=>')
BOOL=re.compile(r'true'|r'false'),
ATOM  =re.compile(  r':[a-zA-Z_][a-zA-Z0-9_]*')
KEY =re.compile(   r'[a-zA-Z_][a-zA-Z0-9_]*:')

