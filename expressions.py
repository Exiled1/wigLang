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


# def stat_function(name):
#     return Group(CaselessKeyword(name) + Group(LPAR + delimitedList(expr) + RPAR))

ref_ = Word(alphas).setResultsName('var_ref')
params = (LPAR + Group(Optional(delimitedList(expr))).setResultsName('params') + RPAR)
# funcCall = Group(Word(alphas) + Group(LPAR + params + RPAR)).setName('func_call')
funcCall = Group(Word(alphas).setResultsName('func_name') + params).setResultsName('func_call')
# if (x > 0)
# else
multOp = oneOf("* /")#.setResultsName('op')
addOp = oneOf("+ -")#.setResultsName('op')
numericLiteral = ppc.number
operand = (funcCall | numericLiteral | ref_)


def cons_arith_exp(ast):
    for k in ast.keys():
        if type(ast[k]) is str:
            continue
        if k == 'bin_op':
            comb = list(ast['bin_op'].items())
            # ast['bin_op'] = cons_arith_exp(ast['bin_op'])
            # lhs = ast['bin_op'][0]
            # op = ast['bin_op'][1]
            # rhs = ast['bin_op'][2]
            # print(type(rhs) )
            # ast[k] = {'lhs': lhs, 'op': op, 'rhs': rhs}
            # print(repr(comb))
            # print(repr(ast['bin_op'][0]), repr(ast['bin_op'][1]), repr(ast['bin_op'][2]))
            for k1,v in comb:
                print(k1,v)

            # comb = list(ast['bin_op']['num'])
            # comb = ast['bin_op']['num']
            # op = comb['op']
            # print(lhs,rhs,op)
    return ast

def action(toks):
    # if toks.getName() != 'func_call':
        # print('HELLO\n',repr(toks),'\nENDHELLO')
        # print('')
    # print('HELLO\n',,'\nENDHELLO')
    return cons_arith_exp(toks)
    # for k in toks.keys():
    #     if type(toks[k]) is str:
    #         continue
    #     if k == 'bin_op':
    #         for k1 in toks[k].keys():
    #             print(toks[k][k1])
            # print(toks[k].keys())
            # print(type(toks[k]))
            # print(toks[k])
        # if k:
        #     print(k)
        #     print(toks[k])
        #     print(toks.getName())
        #     if toks[k] is not str:
        #         print(toks[k].getName())
    return toks

# arithExpr = infixNotation(
#     operand, [(multOp, 2, opAssoc.LEFT), (addOp, 2, opAssoc.LEFT)]
# ).setResultsName('bin_op')# .setParseAction(action)

arithExpr = Group(operand('lhs') + (multOp | addOp)('op') + operand('rhs'))('bin_op')
arithExpr = arithExpr | (LPAR + arithExpr + RPAR)

# arithExpr = arithExpr.

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


# def _parser(ast):
#     for 

if __name__ == '__main__':
    input = 'g(1 - x)'
    p_tree = expr.parseString(input)
    print(p_tree.asDict())
    # print(input)
    # print(repr(p_tree))
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