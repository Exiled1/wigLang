import copy
class Scope:
    def __init__(self, CallMode, ScopeMode):
        self.callMode = CallMode
        self.scopeMode = ScopeMode
        self.variables = []
        # make a dictionary of possible instructions, takes functions, declarations.
    # newScopr =  Scope(self.CallMode, self....)
    # newScope.variables = [*self.varaibles]
    # newScope
    def scope_cpy(self): 
        newScope = Scope(self.callMode, self.scopeMode)
        newScope.variables = copy.deepcopy