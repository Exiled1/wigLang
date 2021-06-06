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

ref_ = Word(alphas).setResultsName('var_ref')
params = Group((LPAR + Group(Optional(delimitedList(expr))) + RPAR))('params')
# funcCall = Group(Word(alphas) + Group(LPAR + params + RPAR)).setName('func_call')
funcCall = Group(Word(alphas).setResultsName('func_name') + params).setResultsName('func_call')
# if (x > 0)
# else
multOp = oneOf("* /")#.setResultsName('op')
addOp = oneOf("+ -")#.setResultsName('op')
numericLiteral = ppc.number
operand = (funcCall | numericLiteral | ref_)

arithExpr = Group(operand('lhs') + (multOp | addOp)('op') + operand('rhs'))('bin_op')
arithExpr = arithExpr | (LPAR + arithExpr + RPAR)

expr_rule = arithExpr | operand

expr << expr_rule


def expression_parser(string):
    return expr.parseString(string)


if __name__ == '__main__':
    input = 'g(1 - x)'
    p_tree = expr.parseString(input)
    print(p_tree.asDict())
