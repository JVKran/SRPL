from lex import token
from parse.nodes import *
from typing import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def incrementTokenIndex(tokenIndex : int, length : int) -> int:
    if tokenIndex >= length - 1:
        return tokenIndex
    return tokenIndex + 1

def factor(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    currentToken = tokenList[tokenIndex]
    if type(currentToken) == token.VariableToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return tokenIndex, VariableNode(currentToken)
    elif type(currentToken) in (token.IntegerToken, token.FloatToken):
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return tokenIndex, NumberNode(currentToken)

def term(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    tokenIndex, res = binaryOperator(tokenList, factor, (token.MultiplyToken, token.DivideToken), tokenIndex)
    return tokenIndex, res

def expression(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    currentToken = tokenList[tokenIndex]

    if type(currentToken) == token.VariableKeywordToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        assert(type(tokenList[tokenIndex]) == token.VariableToken)
        variableName = tokenList[tokenIndex].stringToParse
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        assert(type(tokenList[tokenIndex]) == token.AssignmentToken)
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        expr = expression(tokenList, tokenIndex)
        return tokenIndex, VariableNode(variableName, expr)
    
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
