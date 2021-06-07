from language import *


def _add(a,b):
    return a + b

def make_add(lhs,rhs):
    return Binary(lhs, rhs, '+', _add)

def _mult(a,b):
    return a * b

def _sub(a,b):
    return a - b

def make_mult(lhs,rhs):
    return Binary(lhs, rhs, '*', _mult)

def _gt(a,b):
    return a > b
def _lt(a,b):
    return a < b

def op_func(op):
    if op == '+':
        return _add
    elif op == '*':
        return _mult
    elif op == '-':
        return _sub
    elif op == '>':
        return _gt
    elif op == '<':
        return _lt