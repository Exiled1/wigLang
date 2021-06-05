import re
import numpy as np
from language import *
# from pyparsing import Forward, Word, alphas, alphanums, nums, ZeroOrMore, Literal, Group, Optional, other
import expressions

def flatten(lis):
    arr = np.array(lis)
    flat = arr.flatten()
    return list(flat)

# [Expression()]
# x := f(x+1+a) * x + 1
'''
# Expression body: [
    Mult([
        function call:
        params: 
            Add(Var(x), Add(Var(a),1))
        
    ])
    
    
]
# function call
# 
'''

'''
2 + x + 4 * 9
Add(2, Add(Var(x), Mult(4, 9)))

Mult(FunctionCall('f', [Add(Var(x), Add(Var(a)))])

Every time we encounter a function, split at first comma, then evaluate
recursively

Add(x,y) ~= Binary(x,y,'+',arithmetic._add) ~= arithmetic.make_add(x,y)
f(x+1)
Expression(FunctionCall('f', [Expression(Add(Var('x'), 1))] ))
'''

# def parse_expression(parse_str):
#     lparen = Literal("(").suppress()
#     rparen = Literal(")").suppress()
#     identifier = Word(alphas, alphanums + "_")
#     integer = Word(nums)
#     functor = identifier
    
#     #recursive expression parsing.
#     expression = Forward()
#     arg = Group(expression) | identifier | integer
#     args = arg + ZeroOrMore("," + arg)

#     expression << functor + Group(lparen + Optional(args) + rparen)
    
#     parsed_expression = expression.parseString(parse_str)
#     print(f" parsed Exp: {parsed_expression}")
#     return parsed_expression

def expression_transformer(root):
    for tag,child in root.items():
        if tag == 'func_call':
            func_name = child['func_name']
            params = [expression_transformer(p) for p in child['params']]
            func = Function(func_name,params)
            return func
        elif tag == '':
            return None

def parse_expression(exp_str):
    parsed = expressions.expression_parser(exp_str)
    print(parsed.asDict())
    print(parsed.asList())
    print(parsed.dump())

    # expression_transformer(parsed.asDict())
    return None


def parse_declaration(line):
    declare_and_maybe_assignment_rule = r"((int|bool) +)?([a-z]) *((:=|=)\s(.+))?;"
    match = re.match(declare_and_maybe_assignment_rule, line)
    if match != None:
        groups = match.groups()
        type_ = groups[1]
        name = groups[2]
        value = groups[5]

        ret = []
        decl = Declare(type_,name)
        ass = Assign(name,value) 

        if name and value:
            res = parse_expression(value)
            if type(res) is Expression:
                ass = Assign(name,res)

        ret.append(decl) if type_ and name else ''
        ret.append(ass) if name and value else ''
        if len(ret) == 0:
            print(f'Could not read line:\n{line}')
            return None
        return ret
    return None

def is_declare(line):
    return parse_declaration(line) != None

def is_block(line):
    return line == '{'

def is_function(line):
    return parse_function(line) != None

def parse_function(line):
    function_and_param_def_rule = r'(int|bool) +(\w+)\(((int|bool) +(\w+))?(, *(int|bool) +(\w+))*\)'
    function_param_rule = r'.*\(((\w+\s+\w+)?|(\w+\s+\w+(,\s?\w+\s+\w+)+))\).*'
    match = re.match(function_and_param_def_rule,line)

    if match != None:
        groups = match.groups()
        return_type = groups[0]
        name = groups[1]
        match = re.match(function_param_rule,line)
        params = []
        if match != None:
            groups = match.groups()
            param_string = groups[0]
            if param_string.strip() != '':
                param_strings = param_string.split(',')
                params = [(p[0],p[1]) for p in [pstring.strip().split(' ') for pstring in param_strings]]
        if not (return_type and name and params):
            return None
        fun = Function(return_type, name, params)
        return [Declare('{.}',name),Assign(name,'λ'),fun]
    else:
        return None

def preprocess(source):
    lines = source.split('\n')
    return ''.join(line.strip() for line in lines)

def lineify(processed):
    lines = processed.replace(';',';\n').replace('{','\n{\n').replace('}','\n}\n').split('\n')
    return [line for line in lines if line != '']

def identify_line(line):
    if is_declare(line):
        return parse_declaration(line)
    elif is_function(line):
        return parse_function(line)
    else:
        return None

def parse_lines(lines):
    depth = 1
    block = Block([],depth)
    function = None
    top_block = block
    for line in lines:
        if is_block(line):
            depth += 1
            new_block = Block([],depth)
            if function is None:
                block.add(new_block)
            else:
                function.code_block = new_block
                # function.code_block.depth -= 1
                # depth -= 1
            new_block.super_block = block
            block = new_block
            continue
        elif line == '}':
            block = block.super_block
            depth -= 1
            continue
        ast_node = identify_line(line)
        if is_function(line):
            function = ast_node[2]
        block.add(ast_node) if ast_node != None else ''
    if top_block != block and depth == 0:
        print('Expecting closing \'}\'!')
    return block
