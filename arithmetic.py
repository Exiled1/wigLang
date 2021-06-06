from language import *


def _add(a,b):
    return a + b

def make_add(lhs,rhs):
    return Binary(lhs, rhs, '+', _add)

def _mult(a,b):
    return a + b

def make_mult(lhs,rhs):
    return Binary(lhs, rhs, '*', _mult)


def op_func(op):
    if op == '+':
        return _add
    elif op == '*':
        return _mult