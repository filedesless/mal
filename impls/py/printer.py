from maltypes import *


def pr_str(e: SExp, print_readably: bool = True) -> str:
    match e:
        case Nil():
            return "nil"
        case Integer(i):
            return str(i)
        case Symbol(s):
            return s
        case String(s):
            if print_readably:
                s = s.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')
            return f'"{s}"'
        case Keyword(s):
            return f":{s}"
        case Expr(l):
            return f"({' '.join(map(pr_str, l))})"
        case Vec(l):
            return f"[{' '.join(map(pr_str, l))}]"
        case Map(m):
            return f"{{{ ' '.join(pr_str(k) + ' ' + pr_str(v) for (k, v) in m.items()) }}}"