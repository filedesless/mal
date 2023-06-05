import re
from typing import List
from maltypes import *

class Reader:
    pos: int = 0
    tokens: List[str] = []

    def __init__(self, tokens: List[str]) -> None:
        self.tokens = tokens

    def next(self) -> str | None:
        if token := self.peek():
            self.pos += 1
            return token

    def peek(self) -> str | None:
        if 0 <= self.pos < len(self.tokens):
            return self.tokens[self.pos]


def read_str(s: str) -> SExp:
    return read_form(Reader(tokenize(s)))

def tokenize(s: str):
    return re.findall(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)""", s)

def read_form(reader: Reader) -> SExp:
    delim = {'(': ')', '[': ']', '{': '}'}
    if (token := reader.peek()) in delim:
        reader.next()
        return read_list(reader, delim[token])
    return read_atom(reader)

def pairs(l: List[SExp]):
    if len(l) < 2:
        return []
    k, v, *r = l
    match k:
        case String(_) | Keyword(_):
            return [(k, v)] + pairs(r)
    raise Exception('key must be string or keyword')

def read_list(reader: Reader, delim: str) -> Expr | Vec | Map:
    l: List[SExp] = []
    while reader.peek() != delim:
        l.append(read_form(reader))
    reader.next()
    if delim == ')':
        return Expr(l)
    if delim == ']':
        return Vec(l)
    return Map(dict(pairs(l)))

def read_atom(reader: Reader) -> SExp:
    if not (token := reader.next()):
        raise Exception("unbalanced expression")

    if (token.startswith('-') and token[1:].isnumeric()) or token.isnumeric():
        return Integer(int(token))

    if token.startswith(';') or token == "nil":
        return Nil()
    
    if token.startswith(':'):
        return Keyword(token[1:])
    
    if token.startswith('"'):
        if len(token) < 2 or not token.endswith('"'):
            raise Exception('unbalanced string')
        token = token[1:-1]
        if token.endswith('\\') and not token.endswith('\\\\'):
            raise Exception('unbalanced string')
        i, s, t = 0, "", {'n': '\n', '"': '"', '\\': '\\'}
        while i < len(token):
            if token[i] == '\\':
                if not i + 1 < len(token):
                    raise Exception('unbalanced string')
                s += t.get(token[i + 1], token[i + 1])
                i += 2
            else:
                s += token[i]
                i += 1
        return String(s)
    
    return Symbol(token)