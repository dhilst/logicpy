import re
from itertools import chain
from collections import defaultdict
from dataclasses import dataclass
from pprint import pp, pformat

from lark import Lark, Transformer, v_args
from igraph import Graph, summary, Vertex as _Vertex

class Vertex:
    def __init__(self, v):
        self.v = v

    def __repr__(self):
        return repr(self.v.attributes())

    def __hash__(self):
        return hash(self.v)


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

    def evaluate(self, ast: AST):
        match ast:
            case Exist(vars, body):
                return self.evaluate(body)

            case Fcall("and", args):
                # A list of dics with the results of the evaluations
                results = [self.evaluate(arg) for arg in args]
                env = defaultdict(set)
                for r in results:
                    for k, vals in r.items():
                        values = [r.get(k, set()) for r in results]
                        for v in vals:
                            # If the value is included in all the evaluations
                            # we included in the result this is the AND logic
                            if all(v in vs for vs in values):
                                env[k].add(v)
                return dict(**env)

            case Fcall("or", args):
                # A list of dics with the results of the evaluations
                results = [self.evaluate(arg) for arg in args]
                env = defaultdict(set)
                for r in results:
                    for k, vals in r.items():
                        values = [r.get(k, set()) for r in results]
                        for v in vals:
                            # If the value is included in all the evaluations
                            # we included in the result this is the AND logic
                            if any(v in vs for vs in values):
                                env[k].add(v)
                return dict(**env)

            case Fcall(fname, args):
                if re.match(r"\w+_(eq|ne|lt|le|gt|ge)$", fname) is not None:
                    v, body = args
                    d = {fname: body}
                    return {v.name: set(v for v in self.g.vs.select(**d))}


        assert False, f"TODO interpret {ast}"




logic_parser = Lark(calc_grammar, parser='lalr', transformer=Parser())

def main():
    import sys


    g = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
    g.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
    g.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
    g.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
    g.es["is_formal"] = [False, False, True, True, True, False, True, False, False]
    # exist (v): name_eq(v, "Alice") 
    # AST Exist(vars=[Var(name='v')], body=Fcall(name='name_eq', args=(Var(name='v'), 'Alice')))
    # g.vs.select(name_eq="Alice")
    print("Vertices", pformat(list(g.vs)))
    # ast: AST = logic_parser.parse(sys.stdin.read()) # type: ignore
    query = 'exist (v): and(gender_eq(v, "m"), age_ge(v, 25))'
    print("query", query)
    intp = Interpreter(g)
    pp(intp.evaluate(logic_parser.parse(query))) # type: ignore

    query = 'exist (v): or(name_eq(v, "Alice"), age_lt(v, 25))'
    print("query", query)
    intp = Interpreter(g)
    pp(intp.evaluate(logic_parser.parse(query))) # type: ignore




if __name__ == '__main__':
    main()
