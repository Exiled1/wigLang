import numpy as np
def flatten(lis):
    arr = np.array(lis)
    flat = arr.flatten()
    return list(flat)

class Declare:
    def __init__(self, type_, name):
        self.type = type_
        self.name = name
    def __str__(self):
        return f'{self.type} {self.name};\n'
    def eval(self, scope):
        return scope.set_var(self.name, None)

class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return f'{self.name} := {self.value};\n'
    def eval(self, scope):
        return scope.set_var(self.name, self.value)

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
    
    def eval(self, scope):
        scope_ = scope
        for inst in self.instructions:
            scope_ = inst.eval(scope_)
        return scope

class Function:
    def __init__(self,return_type,name,param_list):
        self.return_type = return_type
        self.name = name
        self.param_list = param_list
        self.code_block = None
    
    def __str__(self):
        params = ', '.join(param[0] + ' ' + param[1] for param in self.param_list)
        return f'{self.return_type} {self.name}({params})\n{str(self.code_block)}'
    
    def eval(self, scope):
        for type_, name in self.param_list:
            scope = scope.push_var(name, None)
        scope = self.code_block.eval(scope)
        for type_, name in self.param_list:
            scope = scope.pop_val(name)
        return scope