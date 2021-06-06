from pyparsing import *

integer = pyparsing_common.signed_integer
varname = pyparsing_common.identifier


op = Group(oneOf('* /') | oneOf('+ -'))
def action(toks):
    print(t[0::2])
    return toks
term = Group(integer | varname)
arith_expr = term('lhs') + OneOrMore(op('op') + term('rhs'))('bin_comb') # infixNotation(integer | varname,

LPAR,RPAR = map(Suppress, '()')
expr = Forward()
operand = integer
factor = Group(operand | Group(LPAR + expr + RPAR))
term = factor + ZeroOrMore( oneOf('* /') + factor )
expr <<= term + ZeroOrMore( oneOf('+ -') + term )

#     [
#     ('-', 1, opAssoc.RIGHT),
#     (oneOf('* /'), 2, opAssoc.LEFT),
#     (oneOf('+ -'), 2, opAssoc.LEFT),
#     ]).setParseAction(action)
tests = [
    '5+3*6'
    '(5+3)*6'
    '-2--11'
]
for test in tests:
    parsed = expr.parseString(test)
    parsed.pprint()
    print(parsed.dump())
    # print(parsed.asList())
    # print(parsed.asDict())