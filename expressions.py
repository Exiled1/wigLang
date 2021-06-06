# excelExpr.py
#
# Copyright 2010, Paul McGuire
#
# A partial implementation of a parser of Excel formula expressions.
#
from pyparsing import (
    CaselessKeyword,
    Suppress,
    Word,
    alphas,
    alphanums,
    nums,
    Optional,
    Group,
    oneOf,
    Forward,
    infixNotation,
    opAssoc,
    dblQuotedString,
    delimitedList,
    Combine,
    Literal,
    QuotedString,
    ParserElement,
    pyparsing_common as ppc,
)

ParserElement.enablePackrat()

EQ, LPAR, RPAR, COLON, COMMA = map(Suppress, "=():,")

expr = Forward()
ref_ = Word(alphas)#('var_ref')
params = (LPAR + Optional(delimitedList(Group(expr))) + RPAR)('params')
# funcCall = Group(Word(alphas) + Group(LPAR + params + RPAR)).setName('func_call')
funcCall = Group(Group(Word(alphas)('func_name') + params)('func_call'))
# if (x > 0)
# else
multOp = oneOf("* /")#.setResultsName('op')
addOp = oneOf("+ -")#.setResultsName('op')
numericLiteral = ppc.number
operand = funcCall | numericLiteral | ref_

arithExpr = (Group(operand('lhs') + (multOp | addOp)('op') + operand('rhs'))('bin_op'))
arithExpr = arithExpr | (LPAR + arithExpr + RPAR)

expr_rule = arithExpr | operand

expr << expr_rule
top = Group(expr)('expr')

def expression_parser(string):
    return top.parseString(string)


if __name__ == '__main__':
    input = 'f()'# 'f(x+2, 2+1, 4+5, f(x+1))'# 'g(2+3, f(x+1))'
    p_tree = top.parseString(input)
    print(p_tree.dump())
