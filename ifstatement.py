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
'''
if expression block {elseif expression block} [else block] 
'''

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

# ------------------- GRAMMAR BEGIN -----------------

# Make some useful tokens to use in the parser.
ParserElement.enablePackrat()

EQ, LPAR, RPAR, COLON, COMMA = map(Suppress, "=():,")


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

# -------------- GRAMMAR END, CODE START -------------