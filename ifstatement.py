
import pyparsing as pp
'''
if expression block {elseif expression block} [else block] 
'''

# Make some useful tokens to use in the parser.
ppc = pp.pyparsing_common
number = ppc.number
exp = pp.Forward()

# these are identifiers for the actual if statement.
LPAR, RPAR, EQ, COMMA, SEMI, COLON = map(
    pp.Suppress, "()=,;:"
)
OPT_SEMI = pp.Optional(SEMI).suppress() # Optional semicolon, jic.


# make a list of if statement keywords. called it kw cuz I have to 
kw = {
    keyword.upper(): pp.Keyword(keyword)
    for keyword in '''\
    if then elseif else true false
    '''.split()
}

vars().update(kw) # update the keywords into a dictionary.

# Grab they keywords and make their token names conditional_keyword, matches out of the keywords in the keyword list.
cond_keyword = pp.MatchFirst(kw.values()).setName("<conditional_keyword>")


statement = pp.Forward()
exp_atom = (
    kw.TRUE
    | kw.FALSE
    | number
    | functioncall
    | var
)
if_stmt = (
    kw.IF
    + exp

)