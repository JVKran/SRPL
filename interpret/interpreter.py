from lex import token
from parse import parser
from typing import TypeVar, Union
from interpret.context import *
from interpret.number import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

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
    elif type(node.operator) == token.EqualityToken:
        result = left.eq(right)
    elif type(node.operator) == token.NonEqualityToken:
        result = left.ne(right)
    elif type(node.operator) == token.LessToken:
        result = left.lt(right)
    elif type(node.operator) == token.GreaterToken:
        result = left.gt(right)
    elif type(node.operator) == token.LessEqualToken:
        result = left.lte(right)
    elif type(node.operator) == token.GreaterEqualToken:
        result = left.gte(right)
    elif type(node.operator) == token.AndToken:
        result = left.anded_by(right)
    elif type(node.operator) == token.OrToken:
        result = left.ored_by(right)
    
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
