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
        if self.type == '{.}':
            return ''
        return f'{self.type} {self.name};\n'
    def eval(self, scope):
        return scope.push_var(self.name, None)
   
class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        if self.value == 'λ':
            return ''
        return f'{self.name} := {self.value};\n'
    def eval(self, scope):
        return scope.set_var(self.name, self.value)

class Var:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def eval(self, scope):
        return scope.get_var(self.name)

class Block:
    def __init__(self, instructions, depth):
        self.instructions = instructions
        self.super_block = None
        self.depth = depth
        self.local_variables = []
    
    def add(self, ast_node): # ast_node is a list remember
        ast_node = flatten([ast_node])
        for ast in ast_node:
            if type(ast) is Declare:
                self.local_variables.append(ast.name)
        # for ast in ast_node:
        #     self.instructions.append(ast) if ast != None else ''
        self.instructions = [*self.instructions, *[a for a in ast_node if a != None]]
    
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
        for inst in self.instructions:
            scope = inst.eval(scope)
            
        for var in self.local_variables:
            scope = scope.pop_var(var)
        return scope

# Expr holds itself and (maybe its scope)
class Expression:
    def __init__(self, child):
        self.child = child
    def __str__(self):
        return str(self.child)
    def eval(self, scope):
        return self.child.eval(scope)

# x := f(x-1) + 4 * 3 - f(x*9)

class FunctionCall: # f(x+1)
    def __init__(self, name, params):
        self.name = name
        self.params = params
    def __str__(self):
        csl = ', '.join(str(param) for param in self.params)
        # if len(self.params) == 1:
        #     csl = str(self.params[0]) 
        return f'{self.name}({csl})'
    def eval(self, scope):
        # Call-By-... #
        func = scope.get_var(self.name)
        result = func.eval(scope, argument_vals=self.params)
        return result

class Binary:
    def __init__(self, lhs, rhs, symbol, func):
        self.lhs = lhs
        self.rhs = rhs
        self.symbol = symbol
        self.func = func
    def __str__(self):
        return f'{str(self.lhs)} {self.symbol} {str(self.rhs)}'
    def eval(self, scope):
        lhs = self.lhs.eval(scope)
        rhs = self.rhs.eval(scope)
        if type(lhs) is int and type(rhs) is int:
            return self.func(lhs, rhs)
        self.lhs = lhs
        self.rhs = rhs
        return self # this could cause reference issues

# (a + b + c) / (c * (c-a) / 2)

class Function:
    def __init__(self,return_type,name,param_list):
        self.return_type = return_type
        self.name = name
        self.param_list = param_list
        self.code_block = None
    
    def __str__(self):
        params = ', '.join(param[0] + ' ' + param[1] for param in self.param_list)
        return f'{self.return_type} {self.name}({params})\n{str(self.code_block)}'
    
    def eval(self, scope, argument_values=[]):
        if not (len(self.param_list) == len(argument_values)):
            print('Arguments supplied do not match arguments required')
            print(f'Expected: {self.param_list}')
            print(f'Given: {argument_values}')
        for type_, name in self.param_list:
            scope = scope.push_var(name, None)
        for i in range(len(argument_values)):
            arg_type, arg_name = self.param_list[i]
            arg_val = argument_values[i]
            scope = scope.set_var(arg_name,arg_val[i])
        scope = self.code_block.eval(scope)
        for type_, name in self.param_list:
            scope = scope.pop_var(name)
        return scope
