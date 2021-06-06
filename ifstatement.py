
import pyparsing as pp
'''
if expression block {elseif expression block} [else block] 
'''
ppc = pp.pyparsing_common
# make a list of if statement keywords.
keywords = {
    keyword.upper(): pp.Keyword(keyword)
    for keyword in '''\
    if then elseif else
    '''.split()
}

vars().update(keywords) # update the keywords into a dictionary.

# Grab they keywords and make their token names conditional_keyword, matches out of the keywords in the keyword list.
cond_keyword = pp.MatchFirst(keywords.values()).setName("<conditional_keyword>")


statement = pp.Forward()
