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

    def __init__(self, token : token.Token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'

class OperatorNode():

    def __init__(self, left_node : 'Node', operator : 'Node', right_node : 'Node'):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operator}, {self.right_node})'

Node = Union[FunctionNode, NumberNode, OperatorNode]

def incrementTokenIndex(tokenIndex : int, length : int) -> int:
    if tokenIndex >= length - 1:
        return tokenIndex
    return tokenIndex + 1

def factor(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    currentToken = tokenList[tokenIndex]
    if type(currentToken) in (token.IntegerToken, token.FloatToken):
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return tokenIndex, NumberNode(currentToken)

def term(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    tokenIndex, res = binaryOperator(tokenList, factor, (token.MultiplyToken, token.DivideToken), tokenIndex)
    return tokenIndex, res

def expression(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    return binaryOperator(tokenList, term, (token.AddToken, token.SubstractToken), tokenIndex)

def binaryOperator(tokenList : List[token.Token], f : Callable[[A, B], C], operations : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    tokenIndex, left = f(tokenList, tokenIndex)

    while type(tokenList[tokenIndex]) in operations:
        operatorToken = tokenList[tokenIndex]
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, right = f(tokenList, tokenIndex)
        left = OperatorNode(left, operatorToken, right)
    return tokenIndex, left

def parse(tokens: List[token.Token]) -> Node:
    index, res = expression(tokens, 0)
    return res
