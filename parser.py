import re
import numpy as np
from language import *
# from pyparsing import Forward, Word, alphas, alphanums, nums, ZeroOrMore, Literal, Group, Optional, other
import expressions
import arithmetic
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

def expression_transformer(root):

    if type(root) is list:
        if len(root) == 1:
            # print('singleton list', root)
            root = root[0]
            return expression_transformer(root)
        elif len(root) == 0:
            return None
        else:
            print('Cannot transform empty list!', root)

    if type(root) is tuple:
        if type(root[0]) is int:
            root = root[1]
        else:
            root = {root[0]: root[1]}
    if type(root) is dict:
        for tag,child in root.items():
            if tag == 'func_call':
                # child = child[0]
                # print(child)
                func_name = child['func_name']
                params = []
                assert type(child['params']) is list
                for p in child['params']:
                    if type(p) is dict:
                        # print('dict!', p)
                        for di in p:
                            params.append(expression_transformer((di,p[di])))
                    else:
                        # print('PTYPE!', type(p),p)
                        params.append(expression_transformer(p))
                func = FunctionCall(func_name,params)
                return func
            elif type(child) is str:
                return Var(child)
            elif type(child) is int:
                return child
            elif tag == 'bin_op':
                lhs = expression_transformer(child['lhs'])
                op = child['op']
                rhs = expression_transformer(child['rhs'])
                return Binary(lhs, rhs, op, arithmetic.op_func(op))
            else:
                print('could not find', tag)
    elif type(root) is str:
        return Var(root)
    elif type(root) is int:
        return root
    else:
        print('could not parse', repr(root))


def parse_expression(exp_str):
    parsed = expressions.expression_parser(exp_str)
    p_dict = parsed.asDict()
    if len(p_dict.items()) == 0:
        p_list = parsed.asList()
        if len(p_list) > 0:
            return Expression(p_list[0])
        else:
            return None
    # print('parser dictionary', p_dict)
    result = Expression(expression_transformer(p_dict))
    # print('result', result)
    return result

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

        # if name and value:
        #     res = parse_expression(value)
        #     if type(res) is Expression:
        #         ass = Assign(name,res)
        if name and value:
            ass = Assign(name,parse_expression(value))

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
        return [Declare('{.}',name),Assign(name,fun),fun]
    else:
        return None

def is_return(line):
    return parse_return(line) != None

def parse_return(line):
    return_statement_rule = r'(return)\ +(.+);'
    match = re.match(return_statement_rule, line)
    if match != None:
        groups = match.groups()
        return_expr = groups[1]
        return_value = parse_expression(return_expr)
        return [return_value]
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
    elif is_return(line):
        return parse_return(line)
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
            function = None
            continue
        ast_node = identify_line(line)
        if is_function(line):
            function = ast_node[2]
        if is_return(line):
            if function:
                function.return_expression = ast_node[0]
            else:
                print('Error! Cannot have a return statement outside a function!')
            continue
        block.add(ast_node) if ast_node != None else ''
    if top_block != block and depth == 0:
        print('Expecting closing \'}\'!')
    return block
