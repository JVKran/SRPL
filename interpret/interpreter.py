from lex import token
from parse import parser
from typing import TypeVar, Union
from interpret.context import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

class Number():

    def __init__(self, value : Union[int, float]):
        self.value = value

    def add(self, other : 'Number') -> 'Number':
        return Number(self.value + other.value)

    def sub(self, other : 'Number') -> 'Number':
        return Number(self.value - other.value)

    def mul(self, other : 'Number') -> 'Number':
        return Number(self.value * other.value)

    def div(self, other : 'Number') -> 'Number':
        return Number(self.value / other.value)

    def setLineNumber(self, number : int):
        self.lineNumber = number

    def __repr__(self) -> str:
        return str(self.value)


def visit(node : parser.Node, context : Context) -> Number:
    function_name = f'visit{type(node).__name__}'
    function = globals()[function_name]
    return function(node, context)

def visitOperatorNode(node : parser.Node, context : Context) -> Number:
    left = visit(node.left_node, context)
    right = visit(node.right_node, context)

    if type(node.operator) == token.AddToken:
        result = left.add(right)
    elif type(node.operator) == token.SubstractToken:
        result = left.sub(right)
    elif type(node.operator) == token.MultiplyToken:
        result = left.mul(right)
    elif type(node.operator) == token.DivideToken:
        result = left.div(right)
    
    # result.setLineNumber(node.token.lineNumber)
    return result

def visitNumberNode(node : parser.Node, context : Context) -> Number:
    number = Number(node.token.stringToParse)
    number.setLineNumber(node.token.lineNumber)
    return number

def visitVariableNode(node : parser.Node, context : Context):
    if node.value == None:
        variableName = node.var_name.stringToParse
        value = context.get_symbol(variableName)
    else:
        variableName = node.var_name
        value = visit(node.value[1], context)
        context.add_symbol(variableName, value)
    return value
