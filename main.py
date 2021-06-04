import re
import numpy as np
from enum import Enum
import parser
import interpreter
# from scope import Scope


def preprocess(source):
    lines = source.split('\n')
    return ''.join(line.strip() for line in lines)


def lineify(processed):
    lines = processed.replace(';',';\n').replace('{','\n{\n').replace('}','\n}\n').split('\n')
    return [line for line in lines if line != '']
  
with open('ex2.txt', 'r') as file:
    source = file.read()
    processed = preprocess(source)
    lines = lineify(processed)
    parsed = parser.parse_lines(lines)
    print(parsed)
    final = interpreter.evaluate(parsed, parser.Scope('',''))
    print(final)
