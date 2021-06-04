import re
import numpy as np
from enum import Enum

#class TokenType
# 
#
def flatten(lis):
    arr = np.array(lis)
    flat = arr.flatten()
    return list(flat)

# file = open("")
lines = [
    "int x := 2;",
    "int x;",
    "int y = 4;",
    "int int x = 2;"
]
matches = [re.match(r"((int|bool) +)?([a-z]) *((:=|=)\s(.+))?;", line) for line in lines]

grouplist = [(match.groups() if match != None else None) for match in matches]
class Scope:
  def __init__(self, CallMode, ScopeMode):
    self.callMode = CallMode
    self.scopeMode = ScopeMode
  #def actRecord(self, )
  def __str__(self):
    return f'Call Mode: {self.callMode}\nScope Mode: {self.scopeMode}'
class Declare:
    def __init__(self, type_, name):
        self.type = type_
        self.name = name
    def __str__(self):
        return f'{self.type} {self.name};\n'

class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return f'{self.name} := {self.value};\n'

class Block:
    def __init__(self, instructions, depth):
        self.instructions = instructions
        self.super_block = None
        self.depth = depth
    def add(self, ast_node):
        ast_node = flatten([ast_node])
        for ast in ast_node:
            self.instructions.append(ast) if ast != None else ''
    def __str__(self):
        tab = '    '
        indentation = ''.join([tab for i in range(0,self.depth)])
        pp_instructions = [str(inst) for inst in self.instructions]
        pp_block = [indentation + stri.strip() + '\n' for stri in pp_instructions if len(stri.strip()) > 0]
        pp_block = ''.join(pp_block)
        inner_indentation = ''.join([tab for i in range(0,self.depth-1)])
        pp_block = ''.join([
                inner_indentation + '{\n',
                pp_block,
                inner_indentation + '};\n'
            ])
        return pp_block

class Function:
    def __init__(self,return_type,name,param_list):
        self.return_type = return_type
        self.name = name
        self.param_list = param_list
        self.code_block = None
    def __str__(self):
        params = ', '.join(param[0] + ' ' + param[1] for param in self.param_list)
        return f'{self.return_type} {self.name}({params})\n'

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
                print(params)
        if not (return_type and name and params):
            return None
        fun = Function(return_type, name, params)
        return [fun]
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
            new_block.super_block = block
            block = new_block
            continue
        elif line == '}':
            block = block.super_block
            depth -= 1
            continue
        ast_node = identify_line(line)
        if is_function(line):
            function = ast_node[0]
        block.add(ast_node) if ast_node != None else ''
    if top_block != block and depth == 0:
        print('Expecting closing \'}\'!')
    return block

def Evaluate(block, scope):
    actRecord = [] # Make an activation record inside the block.
    block.eval()
    # for inst in block.instructions:
    
  
with open('ex1.txt', 'r') as file:
    source = file.read()
    processed = preprocess(source)
    lines = lineify(processed)
    parsed = parse_lines(lines)
    print(parsed)
    # parsed = flatten([line for line in map(identify_line,lines) if line != None])
    # [print(f'{ast_node}') for ast_node in parsed]

# insts = [parse_instruction(l) for l in lines]
# [[print(f'{i}') for i in inst] if inst != None else None for inst in insts]
