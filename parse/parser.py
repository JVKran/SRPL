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

def comp(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    tokenIndex, res = binaryOperator(tokenList, arith_expr, (token.EqualityToken, token.NonEqualityToken, token.LessToken, token.GreaterToken, token.LessEqualToken, token.GreaterEqualToken), tokenIndex)
    return tokenIndex, res

def arith_expr(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    tokenIndex, res = binaryOperator(tokenList, term, (token.AddToken, token.SubstractToken), tokenIndex)
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
        tokenIndex, expr = expression(tokenList, tokenIndex)
        return tokenIndex, VariableNode(variableName, expr)
    elif type(currentToken) == token.IfToken:
        tokenIndex, expr = if_expr(tokenList, tokenIndex)
        return tokenIndex, expr
    
    return binaryOperator(tokenList, comp, (token.AndToken, token.OrToken), tokenIndex)

def if_expr(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    assert(type(tokenList[tokenIndex]) == token.IfToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    tokenIndex, condition = expression(tokenList, tokenIndex)
    assert(type(tokenList[tokenIndex]) == token.ThenToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    tokenIndex, expr = expression(tokenList, tokenIndex)
    return tokenIndex, IfNode(condition, expr)

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
