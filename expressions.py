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
    ZeroOrMore,
    ParseResults,
    pyparsing_common as ppc,
    Keyword,
    MatchFirst
)

ParserElement.enablePackrat()

EQ, LPAR, RPAR, COLON, COMMA = map(Suppress, "=():,")
# keywords for the if statement
kw = {
    k.upper(): Keyword(k)
    for k in """
    if else false true then
    """.split()
}
vars().update(kw) # update dict keywords to work normally.
cond_keyword = MatchFirst(kw.values()).setName("<conditional keyword>")


def func_action(tree):
    # print(tree[0].asDict())
    func_tree = tree[0]['func_call']
    sub_tree = {}
    sub_tree['func_name'] = func_tree['func_name']
    sub_tree['params'] = [p[0] for p in func_tree['params']]
    # print(sub_tree)
    return {'func_call': sub_tree}
    # return tree[0].asDict()


def iden_action(tree):
    return [tree[0][0]]# { 'var_ref': tree[0][0] }

# ------------- START Function/expression 
# ----------- END Function/expression grammar pt 1. 

def unwrap(obj):
    ot = type(obj)
    if ot is int or ot is str:
        return obj
    if ot is list:
        if len(obj) == 1:
            return unwrap(obj[0])
    if ot is tuple:
        return unwrap(obj[0])
    if ot is dict:
        if 'var_ref' in obj.keys():
            return obj['var_ref']
    return None

def flip_left(root):
    if not (type(root) is dict):
        return root
    if 'bin_op' in root.keys():
        root['bin_op'] = flip_left(root['bin_op'])
        return root
    tmp = root['lhs']
    root['lhs'] = flip_left(root['rhs'])
    root['rhs'] = tmp
    return root

def flip_right(root):
    if not (type(root) is dict):
        return root
    if 'bin_op' in root.keys():
        root['bin_op'] = flip_right(root['bin_op'])
        return root
    tmp = root['rhs']
    root['rhs'] = flip_right(root['lhs'])
    root['lhs'] = tmp
    return root

def arith_action(tree):
    counter = -1
    left = False
    dicts = []
    curr = {}
    tmp = tree['bin_op']
    tree['bin_op'] = []
    for t in tmp:
        tree['bin_op'].insert(0,t)

    for term in tree['bin_op']:
        # print(term)
        counter += 1
        if counter % 2 == 0:
            left = not left
            if left:
                curr['rhs'] = term
            else:
                if len(tree['bin_op']) == counter+1:
                    curr['lhs'] = term
                    dicts.append(curr)
                    # print(curr['rhs'])
                    break
                new_curr = { 'rhs' : term }
                curr['lhs'] = {'bin_op':new_curr}
                dicts.append(curr)
                curr = new_curr
                left = True
        else:
            curr['op'] = term
    # sub_tree = flip_right(dicts[0])
    sub_tree = dicts[0]
    if counter < 2 and counter > -1:
        return tree['bin_op']
    if len(sub_tree.items()) == 0:
        return tree
    return {'bin_op': sub_tree}

def condition_action(tree):
    sub_tree = tree.asDict()
    return {'condition': sub_tree['condition']['expr'][0]}

expr = Forward()
ref_ = Group(Word(alphas)('var_ref')).setParseAction(iden_action)
params = (LPAR + Optional(delimitedList(Group(expr))) + RPAR)('params')
# funcCall = Group(Word(alphas) + Group(LPAR + params + RPAR)).setName('func_call')
funcCall = Group(Group(Word(alphas)('func_name') + params)('func_call'))
funcCall = funcCall | (LPAR + funcCall + RPAR)
funcCall = funcCall.setParseAction(func_action)
# if (x > 0)
# else
multOp = oneOf("* /")#.setResultsName('op')
addOp = oneOf("+ -")#.setResultsName('op')
compareOp = oneOf('< > =')
numericLiteral = ppc.number
operand = funcCall | numericLiteral | ref_


arithExpr = (Group(operand + ZeroOrMore((multOp | addOp | compareOp) + operand))('bin_op'))
arithExpr = arithExpr | (LPAR + arithExpr + RPAR)
arithExpr = arithExpr.setParseAction(arith_action)
expr_rule =  arithExpr | operand

expr << expr_rule

top = Group(expr)('expr')

if_stmt = ('if' + Group(top)('condition') + 'then').setParseAction(condition_action)

def expression_parser(string):
    return top.parseString(string)


if __name__ == '__main__':
    # input = 'f(x-3+4)'# 'f(x+2, 2+1, 4+5, f(x+1))'# 'g(2+3, f(x+1))'
    # p_tree = top.parseString(input)
    # print(type(p_tree[0][0]))
    # p_tree.pprint()
    # print(p_tree.asDict())
    # print(p_tree.dump())

    input = 'if 69 < f(x,g(x)) then'
    p_tree = if_stmt.parseString(input)
    p_tree.pprint()