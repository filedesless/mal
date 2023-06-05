import readline
from sys import exit
from reader import read_str
from printer import pr_str
from maltypes import *
from typing import Callable
from functools import reduce
import operator
from math import prod


def READ() -> SExp:
    try:
        return read_str(input('user> '))
    except KeyboardInterrupt:
        print()
        return Nil()
    except EOFError:
        print()
        exit()

REPL_ENV = {
    '+': lambda xs: Integer(sum(x.i for x in xs)),
    '-': lambda xs: Integer(reduce(operator.sub, (x.i for x in xs), 0)),
    '*': lambda xs: Integer(prod(x.i for x in xs)),
    '/': lambda xs: Integer(reduce(operator.ifloordiv, (x.i for x in xs), 1)),
    'exit': lambda _: exit(),
}

def eval_ast(ast: SExp) -> SExp:
    match ast:
        case Symbol(s):
            if s in REPL_ENV:
                return REPL_ENV[s] # type: ignore
            raise Exception(F"undefined symbol '{s}'")
        case Expr(l):
            return Expr(list(map(EVAL, l)))
        case Vec(l):
            return Vec(list(map(EVAL, l)))
        case Map(m):
            return Map({k: EVAL(v) for (k, v) in m.items()})
    return ast

def EVAL(ast: SExp) -> SExp:
    match ast:
        case Expr(l):
            if not l:
                return ast
            evald = Expr(list(map(EVAL, l)))
            return evald.l[0](evald.l[1:]) # type: ignore
    return eval_ast(ast)

def PRINT(t: SExp):
    print(pr_str(t))

def rep():
    try:
        sexp = EVAL(READ())
    except Exception as e:
        print(e)
    else:
        PRINT(sexp)

if __name__ == '__main__':
    print("Welcome to felisp")
    while True:
        rep()