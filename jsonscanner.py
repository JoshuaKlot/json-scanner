from collections import namedtuple
import re

SKIP_RE = re.compile(r'(( |\t)|\#.*)+')
INT_RE = re.compile(r'\d+')
LEFT_SQUARE = re.compile(r'\[')
RIGHT_SQUARE = re.compile(r'\]')
COLON = re.compile(r':')
COMMA = re.compile(r',')
LEFT_CURLY = re.compile(r'\{')
RIGHT_CURLY = re.compile(r'\}')
LEFT_PERCENT_CURLY = re.compile(r'%\{')
ARROW = re.compile(r'=>')
BOOL = re.compile(r'true|false')
ATOM = re.compile(r':[a-zA-Z_][a-zA-Z0-9_]*')
KEY = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*:')

Token = namedtuple('Token', 'kind lexeme pos')

def tokenize(text, pos=0):
    toks = []
    while pos < len(text):
        m = SKIP_RE.match(text, pos)
        if m:
            pos += len(m.group())
        if pos >= len(text):
            break
        if m := LEFT_SQUARE.match(text, pos):
            toks.append(Token('LEFT_SQUARE', m.group(), pos))
            pos += len(m.group())
            inner_tokens, pos = tokenize(text, pos)
            toks.extend(inner_tokens)
        elif m := RIGHT_SQUARE.match(text, pos):
            toks.append(Token('RIGHT_SQUARE', m.group(), pos))
            pos += len(m.group())
            break
        elif m := COMMA.match(text, pos):
            toks.append(Token('COMMA', m.group(), pos))
            pos += len(m.group())
        elif m := COLON.match(text, pos):
            toks.append(Token('COLON', m.group(), pos))
            pos += len(m.group())
        elif m := LEFT_CURLY.match(text, pos):
            toks.append(Token('LEFT_CURLY', m.group(), pos))
            pos += len(m.group())
        elif m := RIGHT_CURLY.match(text, pos):
            toks.append(Token('RIGHT_CURLY', m.group(), pos))
            pos += len(m.group())
        elif m := LEFT_PERCENT_CURLY.match(text, pos):
            toks.append(Token('LEFT_PERCENT_CURLY', m.group(), pos))
            pos += len(m.group())
        elif m := ARROW.match(text, pos):
            toks.append(Token('ARROW', m.group(), pos))
            pos += len(m.group())
        elif m := BOOL.match(text, pos):
            toks.append(Token('BOOL', m.group(), pos))
            pos += len(m.group())
        elif m := ATOM.match(text, pos):
            toks.append(Token('ATOM', m.group(), pos))
            pos += len(m.group())
        elif m := KEY.match(text, pos):
            toks.append(Token('KEY', m.group(), pos))
            pos += len(m.group())
        elif m := INT_RE.match(text, pos):
            toks.append(Token('INT', m.group(), pos))
            pos += len(m.group())
                

        else:
            raise ValueError(f"Invalid character at position {pos}: {text[pos:]}")
    return toks, pos

# Example usage
text = "[1,2,3,[67,545,9],5]"
tokens, _ = tokenize(text)
for token in tokens:
    print(token)

