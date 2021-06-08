import numpy as np
from interpreter import *

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
        if type(self.value) is Function:
            return ''
        return f'{self.name} := {self.value};\n'
    def eval(self, scope):
        value = self.value
        # if type(value) is Expression or type(value) is Binary or type(value) is FunctionCall or type(value) is Thunk:
        while not (type(value) is Function or type(value) is int):
            value = value.eval(scope)# This may be not poggers
            # if type(value) is Thunk:
            #     value = value.eval(scope)
            # print('Evaled to ', value, type(value))
        return scope.set_var(self.name, value)

class Var:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def eval(self, scope):
        value = scope.get_var(self.name)
        # print('Got value!', value)
        return value

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
        pp_instructions = [inst.pp_str() if type(inst) is Function else str(inst) for inst in self.instructions]
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
        scope.stack_push()
        for inst in self.instructions:
            if type(inst) is Function:
                continue
            scope = inst.eval(scope)
            
        for var in self.local_variables:
            scope = scope.pop_var(var)
        scope.stack_pop()
        return scope

# Expr holds itself and (maybe its scope)
class Expression:
    def __init__(self, child):
        if type(child) is str:
            child = Var(child)
        self.child = child
    def __str__(self):
        return str(self.child)
    def eval(self, scope):
        if type(self.child) is int:
            return self.child
        result = self.child.eval(scope)
        if type(result) is int:
            return result
        return result

class Conditional:
    def __init__(self, condition):
        self.condition = condition
        self.consequent = None
        self.alternative = None
    def __str__(self):
        cons_str = str(self.consequent)
        alt_str = str(self.alternative)
        tabs = '    '.join('' for i in range(self.consequent.depth))
        return f'if {str(self.condition)} then \n{cons_str} {tabs} else\n{alt_str}'
    def eval(self,scope):
        assert self.consequent and self.alternative
        cond = self.condition.eval(scope)
        # print(cond)
        if cond:
            scope = self.consequent.eval(scope)
        else:
            scope = self.alternative.eval(scope)
        return scope
    def set_consequent(self, consequent):
        self.consequent = consequent
    def set_alternative(self, alternative):
        self.alternative = alternative


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
        thunks = [Thunk(param, scope) for param in self.params]
        result_scope = func.eval(scope, thunks)
        result = result_scope.get_var('ret')
        result_scope.pop_var('ret')
        return result

def is_expr_prim(e):
    return type(e) is int or type(e) is bool
def is_expr_node(e):
    return type(e) is FunctionCall or type(e) is Expression or type(e) is Binary or type(e) is Var or type(e) is Thunk or is_expr_prim(e)
class Binary:
    def __init__(self, lhs, rhs, symbol, func):
        self.lhs = lhs
        self.rhs = rhs
        self.symbol = symbol
        self.func = func
        lhs_t = type(lhs)
        rhs_t = type(rhs)
        # print(lhs_t, rhs_t)
        # print(self)
        assert is_expr_node(lhs)
        assert is_expr_node(rhs)
    def __str__(self):
        return f'({str(self.lhs)} {self.symbol} {str(self.rhs)})'
    def eval(self, scope):
        lhs = self.lhs
        rhs = self.rhs
        if not is_expr_prim(lhs):
            # lhs = lhs.eval(scope)
            return Binary(lhs.eval(scope),self.rhs,self.symbol,self.func).eval(scope)
        if not is_expr_prim(rhs):
            # rhs = rhs.eval(scope)
            return Binary(lhs,rhs.eval(scope),self.symbol,self.func).eval(scope)
        if is_expr_prim(lhs) and is_expr_prim(rhs):
            val = self.func(lhs, rhs)
            if type(val) is bool:
                return val
            return Expression(val)
        self.lhs = lhs
        self.rhs = rhs
        return Expression(Binary(lhs,rhs,self.symbol,self.func)) # this could cause reference issues

# (a + b + c) / (c * (c-a) / 2)

class Return:
    def __init__(self, return_expression):
        self.return_expression = return_expression
    def __str__(self):
        return f'return {str(self.return_expression)};'
    def eval(self,scope):
        return self.return_expression.eval(scope)


class Function:
    def __init__(self,return_type,name,param_list):
        self.return_type = return_type
        self.name = name
        self.param_list = param_list
        self.code_block = None
        self.return_expression = None
        self.ret = None
    
    def pp_str(self):
        params = ', '.join(param[0] + ' ' + param[1] for param in self.param_list)
        if self.return_expression:
            self.ret = Return(self.return_expression)
            self.code_block.instructions.append(self.ret)
        res = f'{self.return_type} {self.name}({params})\n{str(self.code_block)}'
        if self.ret:
            self.code_block.instructions.remove(self.ret)
        return res

    def __str__(self):
        return 'λ'
    
    def eval(self, scope, thunks=[]):
        if not (len(self.param_list) == len(thunks)):
            print('Arguments supplied do not match arguments required')
            print(f'Expected: {self.param_list}')
            print(f'Given: {thunks}')
        for type_, name in self.param_list:
            scope = scope.push_var(name, None)
        for i in range(len(thunks)):
            arg_type, arg_name = self.param_list[i]
            arg_val = thunks[i]
            arg_val.bind(arg_name)
            # scope = scope.set_var(arg_name,arg_val.bound())
        scope = self.code_block.eval(scope)

        return_value = None
        if self.return_expression:
            return_value = self.return_expression.eval(scope)

        for type_, name in self.param_list:
            scope = scope.pop_var(name)
        if return_value:
            scope = scope.push_var('ret', return_value)
        return scope
