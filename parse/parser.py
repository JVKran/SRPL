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

def incrementTokenIndex(tokenIndex, length):
    if tokenIndex >= length - 1:
        return tokenIndex
    return tokenIndex + 1

def factor(tokenList : List[token.Token], tokenIndex):
    currentToken = tokenList[tokenIndex]
    if type(currentToken) in (token.IntegerToken, token.FloatToken):
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        print(tokenIndex)
        return tokenIndex, NumberNode(currentToken)

def term(tokenList : List[token.Token], tokenIndex):
    tokenIndex, res = binaryOperator(tokenList, factor, (token.MultiplyToken, token.DivideToken), tokenIndex)
    return tokenIndex, res

def expression(tokenList : List[token.Token], tokenIndex):
    return binaryOperator(tokenList, term, (token.AddToken, token.SubstractToken), tokenIndex)

def binaryOperator(tokenList : List[token.Token], function, operations, tokenIndex):
    tokenIndex, left = function(tokenList, tokenIndex)
    print(tokenIndex)

    while type(tokenList[tokenIndex]) in operations:
        operatorToken = tokenList[tokenIndex]
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, right = function(tokenList, tokenIndex)
        left = OperatorNode(left, operatorToken, right)
    return tokenIndex, left

def parse(tokens: List[token.Token]):
    index, res = expression(tokens, 0)
    return res
