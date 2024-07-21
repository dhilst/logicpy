from dataclasses import dataclass
from lark import Lark, Transformer, v_args


@dataclass(frozen=True)
class Expr:
    pass

@dataclass(frozen=True)
class Var(Expr):
    name: str

@dataclass(frozen=True)
class Fcall:
    name: str
    args: list[Expr]

@dataclass(frozen=True)
class Forall:
    vars: list[Expr]
    body: Expr

@dataclass(frozen=True)
class Exist:
    vars: list[Expr]
    body: Expr

calc_grammar = """
    ?start: stmt

    ?stmt: forall | exist
    
    _list{expr, sep}: expr (sep expr)*

    _args: _list{var, ","}

    forall: "forall" "(" _args ")" ":" _expr -> forall
    exist: "exist" "(" _args ")" ":" _expr -> exist
    fcall: NAME "(" _list{_expr, ","} ")" -> fcall
    var: NAME -> var
    _expr: fcall | var | string
    string: STRING -> string


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




logic_parser = Lark(calc_grammar, parser='lalr', transformer=Parser())

def main():
    import sys
    print(logic_parser.parse(sys.stdin.read()))




if __name__ == '__main__':
    main()
