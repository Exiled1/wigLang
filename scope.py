class Scope:
  def __init__(self, CallMode, ScopeMode):
    self.callMode = CallMode
    self.scopeMode = ScopeMode
    self.variables = []
    # make a dictionary of possible instructions, takes functions, declarations.
  def get_var(self): # getter for the var tuples record, [(var:value),...]
    return self.actRecord

  def set_var(self, var,value):
    self.variables.push((var,value))

  def __str__(self):
    keyPairList = []
    for key, value in self.variables:
      kpStr = f'({key}:{value})'
      keyPairList.push(kpStr)
      # todo in here.
    retStr = f'Call Mode: {self.callMode}\nScope Mode: {self.scopeMode}\n'
    retStr += ""
    return retStr