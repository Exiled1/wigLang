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
)

ParserElement.enablePackrat()

EQ, LPAR, RPAR, COLON, COMMA = map(Suppress, "=():,")


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
numericLiteral = ppc.number
operand = funcCall | numericLiteral | ref_

class ExpressionBuilder:
    def __init__(self):
        self.expression_stack = [{}]
        self.current = self.expression_stack[0]
        self.counter = 0
        self.left = True
        self.done = False
    
    def add(self, term):
        if self.done:
            print('error! done!')
        if self.counter % 2 == 0:
            if self.left:
                self.current['lhs'] = term
            else:
                if type(term) is int or type(term) is str:
                    self.current['rhs'] = term
                elif type(term) is list:
                    if type(term[0]) is int or type(term[0]) is str:
                        self.current['rhs'] = term
                else:
                    self.expression_stack.push({})
                    self.current['rhs'] = self.expression_stack[0]
            self.left = not left
        else:
            assert type(term) is str
            self.current['op'] = term
        self.counter += 1
    def get_dict(self):
        return self.expression_stack[-1]

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



def arith_action(tree):
    # if type(tree) is ParseResults:
    #     print(tree.asDict())
    # if type(tree['bin_op']) is ParseResults:
    #     print(tree['bin_op'].asDict())
    counter = -1
    left = False
    dicts = []
    curr = {}
    for term in tree['bin_op']:
        # print(term)
        counter += 1
        if counter % 2 == 0:
            left = not left
            if left:
                curr['lhs'] = term
            else:
                # if type(term) is int or type(term) is str:
                #     curr['rhs'] = term
                #     dicts.append(curr)
                #     continue
                # elif type(term) is list:
                #     if type(term[0]) is int or type(term[0]) is str:
                #         curr['rhs'] = term[0]
                #         dicts.append(curr)
                #         continue
                if len(tree['bin_op']) == counter+1:
                    curr['rhs'] = term
                    dicts.append(curr)
                    # print(curr['rhs'])
                    break
                curr['rhs'] = { 'lhs' : term }
                dicts.append(curr)
                curr = curr['rhs']
                left = True
        else:
            curr['op'] = term
    sub_tree = dicts[0]
    if counter < 2 and counter > -1:
        return tree['bin_op']
    if len(sub_tree.items()) == 0:
        return tree
    return {'bin_op': sub_tree}
# arithExpr = (Group(operand('lhs') + ZeroOrMore((multOp | addOp)('op') + operand('rhs')('rhs')))('bin_op'))
arithExpr = (Group(operand + ZeroOrMore((multOp | addOp) + operand))('bin_op'))
arithExpr = arithExpr | (LPAR + arithExpr + RPAR)
arithExpr = arithExpr.setParseAction(arith_action)
expr_rule =  arithExpr | operand

expr << expr_rule
top = Group(expr)('expr')

def expression_parser(string):
    return top.parseString(string)


if __name__ == '__main__':
    input = '0+f(x-y+3+4)'# 'f(x+2, 2+1, 4+5, f(x+1))'# 'g(2+3, f(x+1))'
    p_tree = top.parseString(input)
    p_tree.pprint()
    # print(p_tree.asDict())
    # print(p_tree.dump())