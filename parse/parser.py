from typing import Callable, Tuple, List, TypeVar
from parse.error import increment
from parse.nodes import *
from lex.token import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def iterateDecorator(f: Callable[[int, List[Token], Token, A], Tuple[int, B]]) -> Tuple[int, B]:
    def iterate(tokenIndex, tokenList, separateToken, *args):
        if type(tokenList[tokenIndex]) != separateToken:
            return tokenIndex, args[0]
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, args = f(tokenIndex, tokenList, separateToken, *args)
        return iterate(tokenIndex, tokenList, separateToken, args)
    return iterate

def incrementTokenIndex(tokenIndex : int, length : int) -> int:
    if tokenIndex >= length - 1:
        return tokenIndex
    return tokenIndex + 1

def factor(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Node]:
    currentToken = tokenList[tokenIndex]
    if type(currentToken) == VariableToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return tokenIndex, VariableNode(currentToken)
    elif type(currentToken) in (IntegerToken, FloatToken):
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return tokenIndex, NumberNode(currentToken)

def term(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Node]:
    return binaryOperator(tokenList, factor, (MultiplyToken, DivideToken), tokenIndex)

def comparison(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Node]:
    return binaryOperator(tokenList, arithmeticExpression, 
            (EqualityToken, NonEqualityToken, LessToken, GreaterToken, LessEqualToken, GreaterEqualToken), tokenIndex)

def arithmeticExpression(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Node]:
    return binaryOperator(tokenList, term, (AddToken, SubstractToken), tokenIndex)

def expression(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Node]:
    currentToken = tokenList[tokenIndex]

    if type(currentToken) == VariableKeywordToken:
        tokenIndex, node = variable(tokenList, tokenIndex)
    elif type(currentToken) == IfToken:
        tokenIndex, node = ifExpr(tokenList, tokenIndex)
    elif type(currentToken) == WhileToken:
        tokenIndex, node = whileExpr(tokenList, tokenIndex)
    elif type(currentToken) == FunctionToken:
        tokenIndex, node = functionDef(tokenList, tokenIndex)
    elif type(currentToken) == ExecuteToken:
        tokenIndex, node = functionCall(tokenList, tokenIndex)
    else:
        tokenIndex, node = binaryOperator(tokenList, comparison, (AndToken, OrToken), tokenIndex)
    return tokenIndex, node

def ifExpr(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Node]:
    tokenIndex = increment(tokenIndex, tokenList, IfToken)
    tokenIndex, condition = expression(tokenList, tokenIndex)
    tokenIndex = increment(tokenIndex, tokenList, ThenToken)
    if type(tokenList[tokenIndex]) == NewlineToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, expr = statements(tokenList, tokenIndex)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
    if type(tokenList[tokenIndex]) == ElseToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        if type(tokenList[tokenIndex]) == NewlineToken:
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
            tokenIndex, elseExpr = statements(tokenList, tokenIndex)
        else:
            tokenIndex, elseExpr = expression(tokenList, tokenIndex)
        tokenIndex = increment(tokenIndex, tokenList, FunctionEndToken)
        return tokenIndex, IfNode(condition, expr, elseExpr)
    tokenIndex = increment(tokenIndex, tokenList, FunctionEndToken)
    return tokenIndex, IfNode(condition, expr)

def whileExpr(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Node]:
    tokenIndex = increment(tokenIndex, tokenList, WhileToken)
    tokenIndex, condition = expression(tokenList, tokenIndex)
    tokenIndex = increment(tokenIndex, tokenList, ThenToken)
    if type(tokenList[tokenIndex]) == NewlineToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, _statements = statements(tokenList, tokenIndex)
        tokenIndex = increment(tokenIndex, tokenList, FunctionEndToken)
        return tokenIndex, WhileNode(condition, _statements)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
        tokenIndex = increment(tokenIndex, tokenList, FunctionEndToken)
        return tokenIndex, WhileNode(condition, expr)

def variable(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Node]:
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    increment(tokenIndex, tokenList, VariableToken)
    variableName = tokenList[tokenIndex].stringToParse
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
    tokenIndex = increment(tokenIndex, tokenList, AssignmentToken)
    tokenIndex, expr = expression(tokenList, tokenIndex)
    return tokenIndex, VariableNode(variableName, expr)

def functionCall(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Node]:

    @iterateDecorator
    def parseArguments(tokenIndex, tokenList, separateToken, arguments = []):
        tokenIndex, intExpr = expression(tokenList, tokenIndex)
        arguments.append(intExpr)
        return tokenIndex, arguments

    tokenIndex = increment(tokenIndex, tokenList, ExecuteToken)
    tokenIndex, expr = expression(tokenList, tokenIndex)
    if type(tokenList[tokenIndex]) == FunctionParameterToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        if type(tokenList[tokenIndex]) == NowToken:
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        else:
            arguments = []
            tokenIndex, intExpr = expression(tokenList, tokenIndex)
            arguments.append(intExpr)
            tokenIndex, arguments = parseArguments(tokenIndex, tokenList, CommaToken, arguments)
            
            tokenIndex = increment(tokenIndex, tokenList, NowToken)
        return tokenIndex, CallNode(expr, arguments)
    else:
        if type(tokenList[tokenIndex]) == NowToken:
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
            return tokenIndex, CallNode(expr, None)

def functionDef(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Node]:

    @iterateDecorator
    def parseArguments(tokenIndex, tokenList, separateToken, arguments = []):
        arguments.append(tokenList[tokenIndex].stringToParse)
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        return tokenIndex, arguments

    tokenIndex = increment(tokenIndex, tokenList, FunctionToken)
    functionName = tokenList[tokenIndex].stringToParse
    tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))

    arguments = []
    if type(tokenList[tokenIndex]) == FunctionParameterToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        if type(tokenList[tokenIndex]) == VariableToken:
            arguments.append(tokenList[tokenIndex].stringToParse)
            tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
            tokenIndex, arguments = parseArguments(tokenIndex, tokenList, AndToken, arguments)

    tokenIndex = increment(tokenIndex, tokenList, FunctionStartToken)

    if type(tokenList[tokenIndex]) == NewlineToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, expr = statements(tokenList, tokenIndex)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
    tokenIndex = increment(tokenIndex, tokenList, FunctionEndToken)
    return tokenIndex, FunctionNode(functionName, arguments, expr)

def statements(tokenList : List[Token], tokenIndex : int, statings = None):

    @iterateDecorator
    def skipLines(tokenIndex, tokenList, separateToken, skippedLines):
        skippedLines += 1
        return tokenIndex, skippedLines

    skippedLines = 0
    tokenIndex, skippedLines = skipLines(tokenIndex, tokenList, NewlineToken, skippedLines)

    if statings == None: 
        statings = []
    elif not skippedLines:
        return tokenIndex, ListNode(statings)

    tokenIndex, state = statement(tokenList, tokenIndex)
    statings.append(state)

    return statements(tokenList, tokenIndex, statings)

def statement(tokenList, tokenIndex):
    if type(tokenList[tokenIndex]) == ReturnToken:
        tokenIndex = incrementTokenIndex(tokenIndex, len(tokenList))
        tokenIndex, expr = expression(tokenList, tokenIndex)
        return tokenIndex, ReturnNode(expr)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
        return tokenIndex, expr

def binaryOperator(tokenList : List[Token], f : Callable[[A, B], C], operations : List[Token], tokenIndex : int) -> Tuple[int, Node]:
    try:
        tokenIndex, left = f(tokenList, tokenIndex)
    except TypeError:
        print("Error in expression at line " + str(tokenList[tokenIndex].lineNumber) + "!")
        print("Tyring to continue as good as possible... (will most likely fail)")
        return tokenIndex, NumberNode(Token(0, tokenList[tokenIndex].lineNumber))

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

def parse(tokens: List[Token]) -> Node:
    index, res = statements(tokens, 0)
    return res
