import copy
from interpreter import *
from language import *
class Scope:
    #Defaults to static call by value.
    def __init__(self, call_mode=CallMode.VALUE, scope_mode=ScopeMode.STATIC,Variables=[]):
        self.call_mode = call_mode
        self.scope_mode = scope_mode
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
        print(self, f'<push ({name}:{str(value)})>')
        return self

    def get_var(self,name):
        idx = self.find_index(name)
        if idx < 0:
            return None
        return self.variables[idx][1]

    # TODO, make copy method.
    def set_var(self, name, value):
        idx = self.find_index(name)
        if idx > -1:
            self.variables[idx] = (name,value)
        else:
            print(f'{name} is not declared!')
            self.push_var(name,value)
        print(self, f'<assign ({name}:{str(value)})>')
        return self
    

    def pop_var(self, name):
        idx = self.find_index(name)
        value = None
        if idx != -1:
            value = self.variables[idx]
            self.variables.remove(value)
        print(self, f'<pop ({name}:{str(value[1])})>')
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