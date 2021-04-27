from lex import token
from typing import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

class FunctionNode():

    def __init__(self, name : str, returnType : str, arguments : List[token.Token]):
        self.name = name
        self.returnType = returnType
        self.arguments = arguments
        self.codeSequence = []

class NumberNode():

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'

class OperatorNode():

    def __init__(self, left_node, operator, right_node):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operator}, {self.right_node})'

def factor(tokenList : List[token.Token]):
    if type(tokenList[0]) in (token.IntegerToken, token.FloatToken):
        tokenList = tokenList[1:]
        return NumberNode(token)

def term(tokenList : List[token.Token]):
    return binaryOperator(tokenList, factor, (token.MultiplyToken, token.DivideToken))

def expression(tokenList : List[token.Token]):
    return binaryOperator(tokenList, term, (token.AddToken, token.SubstractToken))

def binaryOperator(tokenList : List[token.Token], function, operations):
    left = function(tokenList[1:])
    print("Tokenlist:", tokenList)

    while type(tokenList[0]) in operations:
        print("In operations!")
        operatorToken = tokenList[0]
        right = function(tokenList[1:])
        left = OperatorNode(left, operatorToken, right)
    print("Back!")
    return left

def parse(tokens: List[token.Token]):
    res = expression(tokens)
    return res