def evaluate(block, scope):
    actRecord = [] # Make an activation record inside the block.
    block.eval(scope)
    # for inst in block.instructions:
   