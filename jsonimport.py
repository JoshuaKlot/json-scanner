import json
import re
import sys
import os
from collections import namedtuple

######################PARSER##################################


def parse(text):
    toks = tokenize(text)
    toksIndex = 0
    tok = toks[toksIndex]
    print(toks)
    toksIndex += 1
    

    def consume(kind):
        nonlocal tok, toks, toksIndex
        #print(f"consuming {kind} at {tok}")
        if (peek(kind)):
            tok = toks[toksIndex]
            toksIndex += 1
        else:
            error(kind, text)

        
    def peek(kind):
        nonlocal tok
        print(tok)
        return tok.kind == kind



    def parse_sentence(asts):
        if peek('\n'):
            while peek('\n'):
                consume('\n')
            return parse_sentence(asts)
        elif peek('EOF'):
            return asts
        else:
            e=parse_data_literal()
            asts.append(e)
            return parse_sentence(asts)

    def parse_data_literal():
        if peek('LEFT_SQUARE'):
            op=tok.kind
            consume(op)
            p=parse_list_literal()
        elif peek('{'):
            op=tok.kind
            consume(op)
            p=parse_tuple_literal()
        elif peek("%{"):
            op=tok.kind
            consume(op)
            p=parse_map_literal()
        else:
            op=tok.kind
            consume(op)
            p=parse_primitive_literal()
        return p

    def parse_list_literal():
        l=[]
        while not peek("RIGHT_SQUARE"):
            if peek("COMMA"):
                consume("COMMA")
            else:
                p=parse_data_literal()
                l.append(p)

        return {"%k": "list", "%v":[l]}

    def parse_tuple_literal():
        l=[]
        while not peek("}"):
            if peek(","):
                op=tok.kind
                consume(op)
            p=parse_data_literal()
            l.append(p)


        return {"%k": "truple", "%v":[l]}

    def parse_map_literal():
        m=[]
        while not peek("}"):
            if peek(","):
                op=tok.kind
                consume(op)
            p=parse_key_pair()
            m.append(p)
        
        return {"%k": "map", "%v":[m]}

    def parse_key_pair():
        if peek(KEY):
            op=tok.kind
            consume(op)
            key = parse_key(op)
            value=parse_data_literal()   
        else:
            key=parse_data_literal()   
            if peek("=>"):
                op=tok.kind
                consume(op)
                value = parse_data_literal()
            else:
                value = parse_data_literal()
        return [key, value]

    def parse_primitive_literal():
        if peek(INT_RE):
            op=tok.kind
            consume(op)
            v=int(tok.lexeme)
            return parse_int(v)
        elif peek(ATOM):
            op=tok.kind
            consume(op)
            token=tok.lexeme
            return parse_atom(token)
        elif peek(BOOL):
            op=tok.kind
            consume(op)
            b=bool(tok.lexeme)
            return parse_bool(b)
        else:
            raise SyntaxError(f"Unexpected token: {tok.lexeme}")

    def parse_int(value):
        return {"%k": "int", "%v": value}

    def parse_atom(token):
        return {"%k": "atom", "%v": token}
    
    def parse_key(key):
        
        return {"%k": "key", "%v": key}

    def parse_bool(b):
        return {"%k": "bool", "%v": b}
    
    def error(kind, text):
        nonlocal tok
        pos = tok.pos
        if pos >= len(text) or text[pos] == '\n': pos -= 1
        lineBegin = text.rfind('\n', 0, pos)
        if lineBegin < 0: lineBegin = 0
        lineEnd = text.find('\n', pos)
        if lineEnd < 0: lineEnd = len(text)
        line = text[lineBegin:lineEnd]
        print(f"error: expecting '{kind}' but got '{tok.kind}'",
              file=sys.stderr)
        print(line, file=sys.stderr)
        nSpace = pos - lineBegin if pos >= lineBegin else 0
        print('^'.rjust(nSpace+1), file=sys.stderr)
        sys.exit(1)
    
    asts = []
    parse_sentence(asts)
    if tok.kind != 'EOF': error('EOF', text)
    return asts

    ############################LEXER#######################################
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
            tok=(Token('LEFT_SQUARE', m.group(), pos))
            
        elif m := RIGHT_SQUARE.match(text, pos):
            tok=(Token('RIGHT_SQUARE', m.group(), pos))
            
        elif m := ATOM.match(text, pos):
            tok=(Token('ATOM', m.group(), pos))
            
        elif m := COMMA.match(text, pos):
            tok=(Token('COMMA', m.group(), pos))
            
        elif m := COLON.match(text, pos):
            tok=(Token('COLON', m.group(), pos))
            
        elif m := LEFT_CURLY.match(text, pos):
            tok=(Token('LEFT_CURLY', m.group(), pos))
            
        elif m := RIGHT_CURLY.match(text, pos):
            tok=(Token('RIGHT_CURLY', m.group(), pos))
            
        elif m := LEFT_PERCENT_CURLY.match(text, pos):
            tok=(Token('LEFT_PERCENT_CURLY', m.group(), pos))
            
        elif m := ARROW.match(text, pos):
            tok=(Token('ARROW', m.group(), pos))
            
        elif m := BOOL.match(text, pos):
            tok=(Token('BOOL', m.group(), pos))
            
        elif m := KEY.match(text, pos):
            tok=(Token('KEY', m.group(), pos))
            
        elif m := INT_RE.match(text, pos):
            tok=(Token('INT', m.group(), pos))
            
        else:
            raise ValueError(f"Invalid character at position {pos}: {text[pos:]}")
        toks.append(tok)
        pos += len(m.group())
    toks.append(Token('EOF', '<EOF>', pos))
    return toks
    #########################################################################

def main():

    text = "[12]"
    #print(tokenize(text))
    asts = parse(text)
    print(json.dumps(asts, separators=(',', ':'))) #no whitespace

if __name__ == "__main__":
    main()
