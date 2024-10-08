import re
import numpy as np
from enum import Enum
import parser
from logger import *
import interpreter
from scope import Scope
# from scope import Scope


def preprocess(source):
    lines = source.split('\n')
    return ''.join(line.strip() for line in lines)


def lineify(processed):
    lines = processed.replace(';',';\n').replace('{','\n{\n').replace('}','\n}\n').split('\n')
    return [line for line in lines if line != '']
'''
# uncomment to test out expression parser for functions.
# works for: f(x, g(x), y);
# parsed Exp: ['f', ['x', ',', ['g', ['x']], ',', 'y']]
# doesn't work with arithmetic though. like:
# f(x-1, f(x), y);
with open('expr1.txt', 'r') as file:
    expression = file.read()
    parser.parse_expression(expression)
'''
with open('ex4.txt', 'r') as file:
    source = file.read()
    processed = preprocess(source)
    lines = lineify(processed)
    parsed = parser.parse_lines(lines)
    print(parsed)
    final = interpreter.evaluate(parsed, Scope(call_mode=interpreter.CallMode.NEED, scope_mode=interpreter.ScopeMode.STATIC))
    logger_instance._print(changes=True)
    print('Result: ' + str(final))

