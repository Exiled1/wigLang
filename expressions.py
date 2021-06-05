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
EXCL, DOLLAR = map(Literal, "!$")
sheetRef = Word(alphas, alphanums) | QuotedString("'", escQuote="''")
colRef = Optional(DOLLAR) + Word(alphas, max=2)
rowRef = Optional(DOLLAR) + Word(nums)
cellRef = Combine(
    Group(Optional(sheetRef + EXCL)("sheet") + colRef("col") + rowRef("row"))
)


expr = Forward()

COMPARISON_OP = oneOf("< = > >= <= != <>")
condExpr = expr + COMPARISON_OP + expr

ifFunc = (
    CaselessKeyword("if")
    - LPAR
    + Group(condExpr)("condition")
    + COMMA
    + Group(expr)("if_true")
    + COMMA
    + Group(expr)("if_false")
    + RPAR
)


# def stat_function(name):
#     return Group(CaselessKeyword(name) + Group(LPAR + delimitedList(expr) + RPAR))

ref_ = Word(alphas).setResultsName('var_ref')
params = (LPAR + Group(Optional(delimitedList(expr))).setResultsName('params') + RPAR)
# funcCall = Group(Word(alphas) + Group(LPAR + params + RPAR)).setName('func_call')
funcCall = (Word(alphas).setResultsName('func_name') + params).setResultsName('func_call')

multOp = oneOf("* /").setResultsName('op')
addOp = oneOf("+ -").setResultsName('op')
numericLiteral = ppc.number.setResultsName('num')
operand = numericLiteral | funcCall | ref_
arithExpr = (infixNotation(
    operand, [(multOp, 2, opAssoc.LEFT), (addOp, 2, opAssoc.LEFT)]
))

expr_rule = arithExpr | operand


expr << expr_rule


# (EQ + expr).runTests(
#     """\
#     =3*A7+5
#     =3*Sheet1!$A$7+5
#     =3*'Sheet 1'!$A$7+5
#     =3*'O''Reilly''s sheet'!$A$7+5
#     =if(Sum(A1:A25)>42,Min(B1:B25),if(Sum(C1:C25)>3.14, (Min(C1:C25)+3)*18,Max(B1:B25)))
#     =sum(a1:a25,10,min(b1,c2,d3))
#     =if("T"&a2="TTime", "Ready", "Not ready")
# """
# )

# expr.runTests(
# """\
# f(h+2, x)*f(5+g(4*3,3-1))-1
# """)

def expression_parser(string):
    return expr.parseString(string)

if __name__ == '__main__':
    input = 'f(x+1,g(y+1, 3+1))'
    p_tree = expr.parseString(input)

    # print(input)
    print(p_tree.asDict())
    # p_tree.pprint()
    # print(repr(p_tree))
    # p_tree.pprint()

    # def r_print(tree):
    #     try:
    #         return [(print(t) or r_print(t)) for t in tree]
    #     except:
    #         return None

    # print('--------')
    # for t in p_tree:
    #     print(t)