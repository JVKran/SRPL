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
    return binaryOperator(tokenList, factor, (token.MultiplyToken, token.DivideToken), tokenIndex)

def comparison(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    return binaryOperator(tokenList, arithmeticExpression, 
            (token.EqualityToken, token.NonEqualityToken, token.LessToken, token.GreaterToken, token.LessEqualToken, token.GreaterEqualToken), tokenIndex)

def arithmeticExpression(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    return binaryOperator(tokenList, term, (token.AddToken, token.SubstractToken), tokenIndex)

def expression(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    currentToken = tokenList[tokenIndex]

    if type(currentToken) == token.VariableKeywordToken:
        tokenIndex, node = variable(tokenList, tokenIndex)
    elif type(currentToken) == token.IfToken:
        tokenIndex, node = if_expr(tokenList, tokenIndex)
    elif type(currentToken) == token.WhileToken:
        tokenIndex, node = while_expr(tokenList, tokenIndex)
    elif type(currentToken) == token.FunctionToken:
        tokenIndex, node = func_def(tokenList, tokenIndex)
    elif type(currentToken) == token.ExecuteToken:
        tokenIndex, node = call(tokenList, tokenIndex)
    else:
        tokenIndex, node = binaryOperator(tokenList, comparison, (token.AndToken, token.OrToken), tokenIndex)
    return tokenIndex, node

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

def variable(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    assert(type(tokenList[tokenIndex]) == token.VariableToken)
    variableName = tokenList[tokenIndex].stringToParse
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    assert(type(tokenList[tokenIndex]) == token.AssignmentToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    tokenIndex, expr = expression(tokenList, tokenIndex)
    return tokenIndex, VariableNode(variableName, expr)

def call(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:

    def parseArguments(tokenIndex, tokenList, arguments = []):
        if type(tokenList[tokenIndex]) != token.CommaToken:
            return tokenIndex, arguments
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, intExpr = expression(tokenList, tokenIndex)
        arguments.append(intExpr)
        return parseArguments(tokenIndex, tokenList, arguments)

    assert(type(tokenList[tokenIndex]) == token.ExecuteToken)
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    tokenIndex, expr = expression(tokenList, tokenIndex)
    if type(tokenList[tokenIndex]) == token.FunctionParameterToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        if type(tokenList[tokenIndex]) == token.NowToken:
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        else:
            arguments = []
            tokenIndex, intExpr = expression(tokenList, tokenIndex)
            arguments.append(intExpr)
            tokenIndex, arguments = parseArguments(tokenIndex, tokenList, arguments)
            
            assert(type(tokenList[tokenIndex]) == token.NowToken)
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return tokenIndex, CallNode(expr, arguments)
    else:
        if type(tokenList[tokenIndex]) == token.NowToken:
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
            return tokenIndex, CallNode(expr, None)

def func_def(tokenList : List[token.Token], tokenIndex : int) -> Tuple[int, Node]:

    def parseArguments(tokenIndex, tokenList, arguments = []):
        if type(tokenList[tokenIndex]) != token.AndToken:
            return tokenIndex, arguments
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        arguments.append(tokenList[tokenIndex].stringToParse)
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return parseArguments(tokenIndex, tokenList, arguments)

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
            tokenIndex, arguments = parseArguments(tokenIndex, tokenList, arguments)

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

def statements(tokenList : List[token.Token], tokenIndex : int, statings = None):

    def skipLines(tokenIndex, tokenList, skippedLines = 0):
        if type(tokenList[tokenIndex]) != token.NewlineToken:
            return tokenIndex, skippedLines
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        skippedLines += 1
        return skipLines(tokenIndex, tokenList, skippedLines)

    tokenIndex, skippedLines = skipLines(tokenIndex, tokenList)

    if statings == None: 
        statings = []
    elif not skippedLines:
        return tokenIndex, ListNode(statings)

    tokenIndex, state = statement(tokenList, tokenIndex)
    statings.append(state)

    return statements(tokenList, tokenIndex, statings)

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

    def traverse(tokenIndex, left):
        if type(tokenList[tokenIndex]) not in operations:
            return tokenIndex, left
        operatorToken = tokenList[tokenIndex]
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, right = f(tokenList, tokenIndex)
        left = OperatorNode(left, operatorToken, right)
        return traverse(tokenIndex, left)

    tokenIndex, left = traverse(tokenIndex, left)
    return tokenIndex, left

def parse(tokens: List[token.Token]) -> Node:
    index, res = statements(tokens, 0)
    return res
