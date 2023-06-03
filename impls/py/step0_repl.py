import readline
from sys import exit

def read():
    try:
        return input('user> ')
    except (EOFError, KeyboardInterrupt):
        exit()

def eval(x):
    return x

def rep():
    while True:
        print(eval(read()))

if __name__ == '__main__':
    rep()