import copy
from interpreter import *
from language import *
from logger import *

class Binding:
    def __init__(self, name, value, scope):
        self.name = name
        self.value = value
        self.declaration_scope = scope
    def __str__(self):
        return f'{self.name}:{str(self.value)}'
    def __iter__(self):
        yield self.name
        yield self.value
    def can_pop_me(self, current_scope):
        return current_scope is self.declaration_scope

class CaptureGroup:
    def __init__(self, scope):
        self.captured_bindings = scope.variables
        self.call_mode = scope.call_mode
        self.scop_mode = scope.scope_mode

    def get_scope(self):
        scope = Scope(call_mode=self.call_mode,
                        scope_mode=self.scop_mode,
                        variables=self.captured_bindings)
        return scope


class Scope:
    #Defaults to static call by value.
    def __init__(self, call_mode=CallMode.VALUE, scope_mode=ScopeMode.STATIC,variables=[]):
        self.call_mode = call_mode
        self.scope_mode = scope_mode
        self.variables = variables
        # make a dictionary of possible instructions, takes functions, declarations.

    def find_index(self, name):
        i = 0
        for var, val in self.variables:
            if name == var:
                return i
            i += 1
        return -1


    def push_var(self, name, value):
        binding = Binding(name,value,self)
        self.variables.insert(0, binding)
        log(self, f'<push ({name}:{str(value)})>')
        return self

    def get_var(self,name):
        idx = self.find_index(name)
        if idx < 0:
            return None
        return self.variables[idx].value

    # TODO, make copy method.
    def set_var(self, name, value):
        idx = self.find_index(name)
        if idx > -1:
            self.variables[idx].value = value
        else:
            print(f'{name} is not declared!')
            self.push_var(name,value)
        log(self, f'<assign ({name}:{str(value)})>')
        return self
    

    def pop_var(self, name):
        idx = self.find_index(name)
        binding = None
        if idx != -1:
            binding = self.variables[idx]
            if binding.can_pop_me(self):
                self.variables.remove(binding)
                log(self, f'<pop ({name}:{str(binding.value)})>')
        return self
    

    def copy(self):
        return copy.deepcopy(self)
    # from what I can see doing __deepcopy__ will make this class define its own method of deep copying.
    # to use: newScopeObj = copy.deepcopy(oldScopeObj)
    def __deepcopy__(self, memo):
        copiedScope = Scope(self.call_mode, self.scope_mode, copy.deepcopy(self.variables, memo))
        return copiedScope
        # Should return a new scope object with the same variable stack inside of it.

    # Printing method for showing the variable list. 
    def __str__(self):
        keyPairList = [] # ["(key:value)", "(key:value)"]
        for key, value in self.variables:
            if value is None:
                value = '?'
            # kpStr = f'({key}:{value})' # (key:value)
            kpStr = f'{key}:{value}' # (key:value)
            keyPairList.append(kpStr)
        # todo in here.
        retStr = ''
        # retStr = f'Call Mode: {self.call_mode}\nScope Mode: {self.scope_mode}\n'
        retStr += '[' + ', '.join(keyPairList) + ']'
        return retStr
    # newScopr =  Scope(self.call_mode, self....)
    # newScope.variables = [*self.varaibles]
    # newScope