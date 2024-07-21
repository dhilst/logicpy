import sys
from typing import Iterator
import re
from itertools import chain
from collections import defaultdict
from dataclasses import dataclass
from pprint import pp, pformat
from frozendict import frozendict

from lark import Lark, Transformer, v_args
from igraph import Graph, Vertex



@dataclass(frozen=True)
class AST:
    pass

@dataclass(frozen=True)
class Var(AST):
    name: str

@dataclass(frozen=True)
class Fcall:
    name: str
    args: list[AST]

@dataclass(frozen=True)
class Forall:
    vars: list[AST]
    body: AST

@dataclass(frozen=True)
class Exist:
    vars: list[AST]
    body: AST

calc_grammar = """
?start: stmt

?stmt: forall | exist

_list{expr, sep}: expr (sep expr)*

_args: _list{var, ","}

forall: "forall" "(" _args ")" ":" _expr -> forall
exist: "exist" "(" _args ")" ":" _expr -> exist
fcall: NAME "(" _list{_expr, ","} ")" -> fcall
var: NAME -> var
_expr: fcall | var | string | number
string: STRING -> string
number: NUMBER -> number


%import common.CNAME -> NAME
%import common.ESCAPED_STRING -> STRING
%import common.NUMBER
%import common.WS
%ignore WS
"""

@v_args(inline=True)    # Affects the signatures of the methods
class Parser(Transformer):
    def __init__(self):
        pass

    def forall(self, *args):
        *vars, body = args
        return Forall(vars, body)

    def exist(self, *args):
        *vars, body = args
        return Exist(vars, body)

    def var(self, name):
        return Var(name.value)

    def fcall(self, f, *args):
        return Fcall(f.value, args) # type: ignore

    def string(self, value):
        return value.value[1:-1]

    def number(self, value):
        return float(value.value)


class Interpreter:
    def __init__(self, g: Graph):
        self.g = g
        self.env = {}

    def evaluate(self, ast: AST) -> dict[str, set[Vertex]]:
        match ast:
            case Exist(vars, body):
                return self.evaluate(body)

            case Fcall("and", args):
                # A list of dics with the results of the evaluations
                results: Iterator[dict[str, set[Vertex]]] = iter(self.evaluate(arg) for arg in args)
                env: dict[str, list[set[Vertex]]] = defaultdict(list)
                for d in results:
                    for k, v in d.items():
                        env[k].append(v) # type: ignore
                return {k: set.intersection(*v) for k, v in env.items()} # type: ignore

            case Fcall("or", args):
                results: Iterator[dict[str, set]] = iter(self.evaluate(arg) for arg in args)
                env: dict[str, list[set[Vertex]]] = defaultdict(list)
                for d in results:
                    for k, v in d.items():
                        env[k].append(v) # type: ignore
                return {k: set.union(*v) for k, v in env.items()} # type: ignore


            case Fcall(fname, args):

                # dirty hack
                if re.match(r"\w+_(eq|ne|lt|le|gt|ge)$", fname) is not None:
                    v, body = args
                    d = {fname: body}
                    return {v.name: set(frozendict(v.attributes()) for v in self.g.vs.select(**d))}


        assert False, f"TODO interpret {ast}"




logic_parser = Lark(calc_grammar, parser='lalr', transformer=Parser())

def main():
    import sys


    g = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
    g.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
    g.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
    g.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
    g.es["is_formal"] = [False, False, True, True, True, False, True, False, False]
    print("Vertices", pformat(list(g.vs)))
    query = input("> ")
    print("query:: ", query)
    intp = Interpreter(g)
    pp(intp.evaluate(logic_parser.parse(query))) # type: ignore




if __name__ == '__main__':
    main()
