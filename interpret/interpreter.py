from parse.nodes import ReturnNode
from lex import token
from parse import parser
from typing import TypeVar, Union
from interpret.context import *
from interpret.number import *
from interpret.function import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def visit(node : parser.Node, context : Context) -> Number:
    functionName = f'visit{type(node).__name__}'
    function = globals()[functionName]
    return function(node, context)

def visitOperatorNode(node : parser.Node, context : Context) -> Number:
    left = visit(node.left_node, context)
    right = visit(node.right_node, context)
    methodName = f'{type(node.operator).__name__}'.replace("Token", '')
    method = getattr(left, methodName)
    result = method(right)
    
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
        value = visit(node.value, context)
        context.add_symbol(variableName, value)
    return value

def visitIfNode(node, context):
    conditionResult = visit(node.condition, context)
    if conditionResult:
        expressionResult = visit(node.expression, context)
        return expressionResult

    if node.elseExpression:
        elseExpressionResult = visit(node.elseExpression, context)
        return elseExpressionResult

    return None

def visitWhileNode(node, context):
    condition = visit(node.condition, context)
    while condition:
        visit(node.codeSequence, context)
        condition = visit(node.condition, context)
    return None

def visitFunctionNode(node, context):
    name = node.name
    codeSequence = node.codeSequence
    argumentNames = [arg_name for arg_name in node.arguments]
    functionValue = Function(name, codeSequence, argumentNames, context)
    context.add_symbol(name, functionValue)
    return functionValue

def visitCallNode(node, context):
    args = []
    value_to_call = visit(node.node_to_call, context)

    for arg_node in node.arg_nodes:
        args.append(visit(arg_node, context))

    returnValue = value_to_call.execute(args, context)
    return returnValue

def visitListNode(node, context):
    elements = []

    return_present = False
    for element_node in node.element_nodes:
        return_present |= ReturnNode == type(element_node)

    for element_node in node.element_nodes:
        if not return_present:
            elements.append(visit(element_node, context))
        elif type(element_node) == ReturnNode:
            elements.append(visit(element_node, context))
        else:
            visit(element_node, context)
    
    if len(elements) == 1:
        return elements[0]
    return elements

def visitReturnNode(node, context):
    if node.nodeToReturn:
        value = visit(node.nodeToReturn, context)
        return value
    else:
        return None
