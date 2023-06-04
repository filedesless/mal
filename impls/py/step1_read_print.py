import readline
from sys import exit
from reader import read_str
from printer import pr_str
from maltypes import SExp

def READ() -> SExp:
    try:
        return read_str(input('user> '))
    except (EOFError, KeyboardInterrupt):
        print()
        exit()


def EVAL(x):
    return x

def PRINT(t: SExp):
    print(pr_str(t))

def rep():
    while True:
        try:
            PRINT(EVAL(READ()))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    rep()