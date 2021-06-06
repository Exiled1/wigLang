
from enum import Enum

class CallMode(Enum):
    VALUE = 'value'
    NEED = 'need'
    NAME = 'name'

class ScopeMode(Enum):
    STATIC = 'static'
    DYNAMIC = 'dynamic'

class Thunk:
    def __init__(self, expression, scope):
        self.expression = expression
        self.cache = None
        if scope.call_mode == CallMode.VALUE:
            self.cache = expression.eval(scope) if not (type(expression) is int) else expression
    
    def eval(self, scope):
        mode = scope.call_mode
        # value = self.expression.eval(scope)
        # if type(value) is Thunk:
        #     value = value.eval(scope)
        # else:
        #     return value
        if mode == CallMode.VALUE:
            return self.cache
        elif mode == CallMode.NEED:
            if self.cache == None:
                self.cache = self.expression.eval(scope)
            return self.cache
        elif mode == CallMode.NAME:
            return self.expression.eval(scope)
        print('NULL')
        return None

    def bound(self):
        if self.cache:
            return self.cache
        return self

    def __str__(self):
        value = ''
        if self.cache:
            value = str(self.cache)
        else:
            value = str(self.expression)
        return f'(⊢ {value} ⊣)'


def evaluate(block, scope):
    actRecord = [] # Make an activation record inside the block.
    return block.eval(scope)
    # for inst in block.instructions:

   