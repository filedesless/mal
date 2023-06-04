from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Nil:
    pass

@dataclass
class Integer:
    i: int

@dataclass
class String:
    s: str

    def __hash__(self) -> int:
        return hash(self.s)

@dataclass
class Symbol:
    s: str

@dataclass
class Keyword:
    s: str

    def __hash__(self) -> int:
        return hash(self.s)

@dataclass
class Expr:
    l: List['SExp']

@dataclass
class Vec:
    l: List['SExp']

@dataclass
class Map:
    m: Dict[String | Keyword, 'SExp']

SExp = Nil | Integer | String | Symbol | Keyword | Expr | Vec | Map