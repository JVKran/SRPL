from parse.nodes import ReturnNode
from lex import token
from parse import parser
from typing import TypeVar, Union, Optional, Callable, List
from operator import is_not, add
from functools import partial
import itertools
from interpret.context import *
from interpret.number import *
from interpret.function import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def foldl(f: Callable[[A, B], C], base : B, list : List[A]) -> List[C]:
    if not list:
        return base
    head, *tail = list
    return (f(head, foldl(f, base, tail)))

def visit(node : parser.Node, context : Context) -> Number:
    functionName = f'visit{type(node).__name__}'

    def visitOperatorNode(node : parser.OperatorNode, context : Context) -> Number:
        left = visit(node.left_node, context)
        right = visit(node.right_node, context)
        methodName = f'{type(node.operator).__name__}'.replace("Token", '')
        method = getattr(left, methodName)
        return method(right)

    def visitNumberNode(node : parser.NumberNode, context : Context) -> Number:
        return Number(node.token.stringToParse, node.token.lineNumber)

    def visitVariableNode(node : parser.VariableNode, context : Context) -> Number:
        if node.value == None:
            variableName = node.var_name.stringToParse
            value = context.getSymbol(variableName)
        else:
            variableName = node.var_name
            value = visit(node.value, context)
            context.symbols[variableName] = value
        return value

    def visitIfNode(node : parser.IfNode, context : Context) -> Optional[Number]:
        conditionIsMet = visit(node.condition, context)
        if conditionIsMet:
            expressionResult = visit(node.expression, context)
            return expressionResult
        elif node.elseExpression:
            elseExpressionResult = visit(node.elseExpression, context)
            return elseExpressionResult
        return None

    def visitWhileNode(node : parser.WhileNode, context : Context) -> None:
        conditionIsMet = visit(node.condition, context)
        if conditionIsMet:
            visit(node.codeSequence, context)
            return visitWhileNode(node, context)
        else:
            return None

    def visitFunctionNode(node : parser.FunctionNode, context : Context) -> Function:
        name = node.name
        codeSequence = node.codeSequence
        argumentNames = node.arguments
        functionValue = Function(name, codeSequence, argumentNames, context)
        context.symbols[name] = functionValue
        return functionValue

    def visitCallNode(node : parser.CallNode, context : Context) -> Optional[Number]:
        arguments = []
        valueToCall = visit(node.node_to_call, context)

        if node.arg_nodes != None:
            arguments = list(itertools.chain(*map(lambda node: [*arguments, visit(node, context)], node.arg_nodes)))

        return valueToCall.execute(arguments, context)

    def visitListNode(node : parser.ListNode, context : Context) -> Union[Number, List[Number]]:
        returnNodes = map(lambda element: ReturnNode == type(element), node.element_nodes)
        returnPresent = foldl(add, 0, returnNodes)
        
        def visitElement(element_node):
            if not returnPresent:
                return visit(element_node, context)
            elif type(element_node) == ReturnNode:
                return visit(element_node, context)
            visit(element_node, context)

        elements = []
        elements = list(itertools.chain(*map(lambda node: [*elements, visitElement(node)], node.element_nodes)))
        elements = list(filter(partial(is_not, None), elements))
        
        if len(elements) == 1:
            return elements[0]
        return elements

    def visitReturnNode(node : parser.ReturnNode, context : Context) -> Optional[Number]:
        if node.nodeToReturn:
            value = visit(node.nodeToReturn, context)
            return value

    function = locals()[functionName]
    return function(node, context)
