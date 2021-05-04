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
    elif type(currentToken) == token.WhileToken:
        tokenIndex, expr = while_expr(tokenList, tokenIndex)
        return tokenIndex, expr
    elif type(currentToken) == token.FunctionToken:
        tokenIndex, expr = func_def(tokenList, tokenIndex)
        return tokenIndex, expr
    elif type(currentToken) == token.ExecuteToken:
        tokenIndex, expr = call(tokenList, tokenIndex)
        return tokenIndex, expr

    return binaryOperator(tokenList, comp, (token.AndToken, token.OrToken), tokenIndex)

def if_expr(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    assert(type(tokenList[tokenIndex]) == token.IfToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    tokenIndex, condition = expression(tokenList, tokenIndex)
    assert(type(tokenList[tokenIndex]) == token.ThenToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    if type(tokenList[tokenIndex]) == token.NewlineToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, expr = statements(tokenList, tokenIndex)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
    if type(tokenList[tokenIndex]) == token.ElseToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        if type(tokenList[tokenIndex]) == token.NewlineToken:
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
            tokenIndex, elseExpr = statements(tokenList, tokenIndex)
        else:
            tokenIndex, elseExpr = expression(tokenList, tokenIndex)
        assert(type(tokenList[tokenIndex]) == token.FunctionEndToken)
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return tokenIndex, IfNode(condition, expr, elseExpr)
    assert(type(tokenList[tokenIndex]) == token.FunctionEndToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    return tokenIndex, IfNode(condition, expr)

def while_expr(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    assert(type(tokenList[tokenIndex]) == token.WhileToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    tokenIndex, condition = expression(tokenList, tokenIndex)
    assert(type(tokenList[tokenIndex]) == token.ThenToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    if type(tokenList[tokenIndex]) == token.NewlineToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, stateMents = statements(tokenList, tokenIndex)
        assert(type(tokenList[tokenIndex]) == token.FunctionEndToken)
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return tokenIndex, WhileNode(condition, stateMents)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
        assert(type(tokenList[tokenIndex]) == token.FunctionEndToken)
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return tokenIndex, WhileNode(condition, expr)

def call(tokenList, tokenIndex) -> Tuple[int, Node]:
    assert(type(tokenList[tokenIndex]) == token.ExecuteToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    tokenIndex, expr = expression(tokenList, tokenIndex)
    if type(tokenList[tokenIndex]) == token.FunctionParameterToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        arguments = []
        if type(tokenList[tokenIndex]) == token.NowToken:
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        else:
            tokenIndex, intExpr = expression(tokenList, tokenIndex)
            arguments.append(intExpr)

            while type(tokenList[tokenIndex]) == token.CommaToken:
                tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
                tokenIndex, intExpr = expression(tokenList, tokenIndex)
                arguments.append(intExpr)
            
            assert(type(tokenList[tokenIndex]) == token.NowToken)
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return tokenIndex, CallNode(expr, arguments)
    else:
        if type(tokenList[tokenIndex]) == token.NowToken:
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
            return tokenIndex, CallNode(expr, None)
    return tokenIndex, expr


def func_def(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    assert(type(tokenList[tokenIndex]) == token.FunctionToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    functionName = tokenList[tokenIndex].stringToParse
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))

    arguments = []
    if type(tokenList[tokenIndex]) == token.FunctionParameterToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        if type(tokenList[tokenIndex]) == token.VariableToken:
            arguments.append(tokenList[tokenIndex].stringToParse)
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))

            while type(tokenList[tokenIndex]) == token.AndToken:
                tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
                arguments.append(tokenList[tokenIndex].stringToParse)
                tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))

    assert(type(tokenList[tokenIndex]) == token.FunctionStartToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))

    if type(tokenList[tokenIndex]) == token.NewlineToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, expr = statements(tokenList, tokenIndex)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
    assert(type(tokenList[tokenIndex]) == token.FunctionEndToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    return tokenIndex, FunctionNode(functionName, arguments, expr)

def statements(tokenList : List[token.Token], tokenIndex : int):
    statements = []

    while type(tokenList[tokenIndex]) == token.NewlineToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))

    tokenIndex, stateMent = statement(tokenList, tokenIndex)
    statements.append(stateMent)

    more_statements = True

    while True:
        newline_count = 0
        while type(tokenList[tokenIndex]) == token.NewlineToken:
            lastTokenIndex = tokenIndex
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
            newline_count += 1
        if newline_count == 0:
            more_statements = False


        if not more_statements: break
        lastTokenIndex = tokenIndex
        tokenIndex, stateMent = statement(tokenList, tokenIndex)
        more_statements = not (lastTokenIndex == tokenIndex)
        statements.append(stateMent)

    return tokenIndex, ListNode(statements)

def statement(tokenList, tokenIndex):
    if type(tokenList[tokenIndex]) == token.ReturnToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, expr = expression(tokenList, tokenIndex)
        return tokenIndex, ReturnNode(expr)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
        return tokenIndex, expr


def binaryOperator(tokenList : List[token.Token], f : Callable[[A, B], C], operations : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    tokenIndex, left = f(tokenList, tokenIndex)

    while type(tokenList[tokenIndex]) in operations:
        operatorToken = tokenList[tokenIndex]
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, right = f(tokenList, tokenIndex)
        left = OperatorNode(left, operatorToken, right)
    return tokenIndex, left

def parse(tokens: List[token.Token]) -> Node:
    index, res = statements(tokens, 0)
    return res
