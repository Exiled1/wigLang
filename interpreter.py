def evaluate(block, scope):
    actRecord = [] # Make an activation record inside the block.
    return block.eval(scope)
    # for inst in block.instructions:

   