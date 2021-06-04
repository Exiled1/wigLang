import re
import numpy as np
from enum import Enum
from language import *



def flatten(lis):
    arr = np.array(lis)
    flat = arr.flatten()
    return list(flat)

class Scope:
    def __init__(self, CallMode, ScopeMode):
        self.callMode = CallMode
        self.scopeMode = ScopeMode
        self.variables = []
        # make a dictionary of possible instructions, takes functions, declarations.

    def find_index(self, name):
        i = 0
        for var, val in self.variables:
            if name == var:
                return i
            i += 1
        return -1


    def push_var(self, name, value):
        self.variables.insert(0, (name,value))
        return self


    # TODO, make copy method.
    def set_var(self, name, value):
        idx = self.find_index(name)
        if idx > -1:
            self.variables[idx] = (name,value)
        else:
            self.push_var(name,value)
        print(self)
        return self
    

    def pop_val(self, name):
        if (idx := self.find_index(name)) > -1:
            self.variables.remove(self.variables[idx])
        return self
    
    
    # Printing method for showing 
    def __str__(self):
        keyPairList = [] # ["(key:value)", "(key:value)"]
        for key, value in self.variables:
            kpStr = f'({key}:{value})' # (key:value)
            keyPairList.append(kpStr)
        # todo in here.
        retStr = ''
        # retStr = f'Call Mode: {self.callMode}\nScope Mode: {self.scopeMode}\n'
        retStr += '[' + ', '.join(keyPairList) + ']'
        return retStr
    # newScopr =  Scope(self.CallMode, self....)
    # newScope.variables = [*self.varaibles]
    # newScope


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
