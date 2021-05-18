from typing import Callable, Tuple, List, TypeVar
from parse.error import increment
from parse.nodes import *
from lex.token import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

# iterateDecorator :: Callable -> Callable
def iterateDecorator(f: Callable[[int, List[Token], Token, A], Tuple[int, B]]) -> Callable[[int, List[Token], Token, A], Tuple[int, B]]:
    """ Iterate decorator
    Decorator to use for incrementally calling functions until a separater token is reached. 
    
    Parameters:
        f (Callable): The function to execute at every index.
    
    Returns:
        Callable: The decorator to use on a function.
    """
    def iterate(tokenIndex: int, tokenList: List[Token], separateToken: Token, *args: Tuple) -> Tuple[int, B]:
        if type(tokenList[tokenIndex]) != separateToken:
            return tokenIndex, args[0]
        tokenIndex = increment(tokenIndex, tokenList)
        tokenIndex, args = f(tokenIndex, tokenList, separateToken, *args)
        return iterate(tokenIndex, tokenList, separateToken, args)
    return iterate

# factor :: [Token] -> Integer -> Tuple
def factor(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Union[VariableNode, NumberNode]]:
    """ Parse factor
    This function parses a factor; either a variable or a literal integer or float.

    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        Node: A variable- or numbernode.
    """
    currentToken = tokenList[tokenIndex]
    if type(currentToken) == VariableToken:
        tokenIndex = increment(tokenIndex, tokenList)
        return tokenIndex, VariableNode(currentToken)
    elif type(currentToken) in (IntegerToken, FloatToken):
        tokenIndex = increment(tokenIndex, tokenList)
        return tokenIndex, NumberNode(currentToken)

# term :: [Token] -> Integer -> Tuple
def term(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Union[VariableNode, NumberNode]]:
    """ Parse term
    This function parses the result of a term. That's either a variable or a number.

    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        Node: The result of a term; a variable- or numbernode. 
    """
    return binaryOperator(tokenList, factor, (MultiplyToken, DivideToken), tokenIndex)

# comparison :: [Token] -> Integer -> Tuple
def comparison(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Union[VariableNode, NumberNode, OperatorNode]]:
    """ Parse comparisong
    This function returns (a part of) an arithmetic expression. This can either be a
    variable, number or operator node.

    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        Node: (A part of) an arithmetic expression; a variable, number or nodes with operator (if partial). 
    """
    return binaryOperator(tokenList, arithmeticExpression, 
            (EqualityToken, NonEqualityToken, LessToken, GreaterToken, LessEqualToken, GreaterEqualToken), tokenIndex)

# arithmeticExpression :: [Token] -> Integer -> Tuple
def arithmeticExpression(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Union[VariableNode, NumberNode, OperatorNode]]:
    """ Parse arithmetic expression
    This function parses an arithmetic expression and returns the result of this expression. This
    can either be a variable, number or operator node.

    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index. 
        Node: (A part of) the result of an arithmetic expression; a variable, number or nodes with operator (if partial). 
    """
    return binaryOperator(tokenList, term, (AddToken, SubstractToken), tokenIndex)

# expression :: [Token] -> Integer -> Tuple
def expression(tokenList : List[Token], tokenIndex : int) -> Tuple[int, Node]:
    """ Parse an expression
    This function parses an expression in the broadest term possible. Can be either of a variable,
    if-statement, while-loop, function definition, function call or an operator.

    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        Node: A (partial) result of an expression.
    """
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

# ifExpr :: [Token] -> Integer -> Tuple
def ifExpr(tokenList : List[Token], tokenIndex : int) -> Tuple[int, IfNode]:
    """ Parse if-statement
    This function parses an if-statement and (when given) also the else-expression.

    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        IfNode: An IfNode with the condition, expression and optional else expression. 
    """
    tokenIndex = increment(tokenIndex, tokenList, IfToken)
    tokenIndex, condition = expression(tokenList, tokenIndex)
    tokenIndex = increment(tokenIndex, tokenList, ThenToken)
    if type(tokenList[tokenIndex]) == NewlineToken:
        tokenIndex = increment(tokenIndex, tokenList)
        tokenIndex, expr = statements(tokenList, tokenIndex)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
    if type(tokenList[tokenIndex]) == ElseToken:
        tokenIndex = increment(tokenIndex, tokenList)
        if type(tokenList[tokenIndex]) == NewlineToken:
            tokenIndex = increment(tokenIndex, tokenList)
            tokenIndex, elseExpr = statements(tokenList, tokenIndex)
        else:
            tokenIndex, elseExpr = expression(tokenList, tokenIndex)
        tokenIndex = increment(tokenIndex, tokenList, FunctionEndToken)
        return tokenIndex, IfNode(condition, expr, elseExpr)
    tokenIndex = increment(tokenIndex, tokenList, FunctionEndToken)
    return tokenIndex, IfNode(condition, expr)

# whileExpr :: [Token] -> Integer -> Tuple
def whileExpr(tokenList : List[Token], tokenIndex : int) -> Tuple[int, WhileNode]:
    """ Parse while-loop
    This function parses a while-loop with corresponding condition.

    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        WhileNode: A WhileNode with the expression to execute as long as the condition is met.
    """
    tokenIndex = increment(tokenIndex, tokenList, WhileToken)
    tokenIndex, condition = expression(tokenList, tokenIndex)
    tokenIndex = increment(tokenIndex, tokenList, ThenToken)
    if type(tokenList[tokenIndex]) == NewlineToken:
        tokenIndex = increment(tokenIndex, tokenList)
        tokenIndex, _statements = statements(tokenList, tokenIndex)
        tokenIndex = increment(tokenIndex, tokenList, FunctionEndToken)
        return tokenIndex, WhileNode(condition, _statements)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
        tokenIndex = increment(tokenIndex, tokenList, FunctionEndToken)
        return tokenIndex, WhileNode(condition, expr)

# variable :: [Token] -> Integer -> Tuple
def variable(tokenList : List[Token], tokenIndex : int) -> Tuple[int, VariableNode]:
    """ Parse variables
    This function parses variables and their assignments.

    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        VariableNode: a VariableNode with the name and value or expression for determining value. """
    tokenIndex = increment(tokenIndex, tokenList)
    increment(tokenIndex, tokenList, VariableToken)
    variableName = tokenList[tokenIndex].stringToParse
    tokenIndex = increment(tokenIndex, tokenList)
    tokenIndex = increment(tokenIndex, tokenList, AssignmentToken)
    tokenIndex, expr = expression(tokenList, tokenIndex)
    return tokenIndex, VariableNode(variableName, expr)

# functionCall :: [Token] -> Integer -> Tuple
def functionCall(tokenList : List[Token], tokenIndex : int) -> Tuple[int, CallNode]:
    """ Parse functioncall
    This function parses a functioncall with corresponding arguments and 
    their values.

    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        CallNode: A CallNode with the given name and arguments to execute it with. 
    """

    @iterateDecorator
    # parseArguments :: Integer -> [Token] -> Token -> List -> Tuple
    def parseArguments(tokenIndex: int, tokenList: List[Token], separateToken: Token, arguments: List[Node] = []) -> Tuple[int, List[Node]]:
        tokenIndex, intExpr = expression(tokenList, tokenIndex)
        arguments.append(intExpr)
        return tokenIndex, arguments

    tokenIndex = increment(tokenIndex, tokenList, ExecuteToken)
    tokenIndex, name = expression(tokenList, tokenIndex)
    if type(tokenList[tokenIndex]) == FunctionParameterToken:
        tokenIndex = increment(tokenIndex, tokenList)
        if type(tokenList[tokenIndex]) == NowToken:
            tokenIndex = increment(tokenIndex, tokenList)
        else:
            arguments = []
            tokenIndex, intExpr = expression(tokenList, tokenIndex)
            arguments.append(intExpr)
            tokenIndex, arguments = parseArguments(tokenIndex, tokenList, CommaToken, arguments)
            
            tokenIndex = increment(tokenIndex, tokenList, NowToken)
        return tokenIndex, CallNode(name, arguments)
    else:
        if type(tokenList[tokenIndex]) == NowToken:
            tokenIndex = increment(tokenIndex, tokenList)
            return tokenIndex, CallNode(name, None)

# functionDef :: [Token] -> Integer -> Tuple
def functionDef(tokenList : List[Token], tokenIndex : int) -> Tuple[int, FunctionNode]:
    """ Parse function definition
    This function parses a function definition including their corresponding
    argumentnames and codeSequences.

    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        FunctionNode: A FunctionNode with name, argument names and sequence to execute on execution. 
    """

    @iterateDecorator
    def parseArguments(tokenIndex: int, tokenList: List[Token], separateToken: Token, arguments: List[Node] = []) -> Tuple[int, List[Node]]:
        arguments.append(tokenList[tokenIndex].stringToParse)
        tokenIndex = increment(tokenIndex, tokenList)
        return tokenIndex, arguments

    tokenIndex = increment(tokenIndex, tokenList, FunctionToken)
    functionName = tokenList[tokenIndex].stringToParse
    tokenIndex = increment(tokenIndex, tokenList)

    arguments = []
    if type(tokenList[tokenIndex]) == FunctionParameterToken:
        tokenIndex = increment(tokenIndex, tokenList)
        if type(tokenList[tokenIndex]) == VariableToken:
            arguments.append(tokenList[tokenIndex].stringToParse)
            tokenIndex = increment(tokenIndex, tokenList)
            tokenIndex, arguments = parseArguments(tokenIndex, tokenList, AndToken, arguments)

    tokenIndex = increment(tokenIndex, tokenList, FunctionStartToken)

    if type(tokenList[tokenIndex]) == NewlineToken:
        tokenIndex = increment(tokenIndex, tokenList)
        tokenIndex, expr = statements(tokenList, tokenIndex)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
    tokenIndex = increment(tokenIndex, tokenList, FunctionEndToken)
    return tokenIndex, FunctionNode(functionName, arguments, expr)

# statements :: [Token] -> Integer -> [Node] -> Tuple
def statements(tokenList : List[Token], tokenIndex : int, statings: List[Node] = None) -> Tuple[int, Node]:
    """ Parse statements
    This function might be described as the heart of the parser for multi-line statements.
    Hence, it's especially useful for interpreting files; it splits the entire file into
    multiple multi-line statements. Each of those statements is executed; one by one.

    So actually, the parser for files is the same as the parser used for the shell; the file
    contains multiple entries that can also be typed in the shell one by one. It keeps parsing
    the file until there are no more lines to be skipped.

    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        Node: The List(Root)Node with all statements to execute.
    """

    @iterateDecorator
    def skipLines(tokenIndex: int, tokenList: List[Token], separateToken: Token, skippedLines: int) -> Tuple[int, int]:
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

# statement :: [Token] -> Integer -> Tuple
def statement(tokenList: List[Token], tokenIndex: int) -> Tuple[int, Node]:
    """ Parse statement
    Gets called by statements() to get each individual statement. 
    
    Parameters:
        tokenList (List): The list with tokens to parse.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        Node: The parsed statement (expression).
    """
    if type(tokenList[tokenIndex]) == ReturnToken:
        tokenIndex = increment(tokenIndex, tokenList)
        tokenIndex, expr = expression(tokenList, tokenIndex)
        return tokenIndex, ReturnNode(expr)
    else:
        tokenIndex, expr = expression(tokenList, tokenIndex)
        return tokenIndex, expr

# binaryOperator :: [Token] -> Callable -> [Token] -> Integer -> Tuple
def binaryOperator(tokenList : List[Token], f : Callable[[A, B], C], operations : List[Token], tokenIndex : int) -> Tuple[int, Union[VariableNode, NumberNode, OperatorNode]]:
    """ Parse binary operator 
    Creates OperatorNode with operator and left and right node to execute it on. 
    
    Parameters:
        tokenList (List): The list with tokens to parse.
        f (Callable): The function to execute for getting left and right node on which operator should be executed.
        operations (List): The list with operators which this function is 'allowed' to be.
        tokenIndex (int): The current index at which we're parsing the tokenList.
    
    Returns:
        int: The incremented token index.
        Node: The operator-, left- or right node.
    """
    try:
        tokenIndex, left = f(tokenList, tokenIndex)
    except TypeError:
        print("Error in expression at line " + str(tokenList[tokenIndex].lineNumber) + "!")
        print("Tyring to continue as good as possible... (will most likely fail)")
        return tokenIndex, NumberNode(Token(0, tokenList[tokenIndex].lineNumber))

    def traverse(tokenIndex : int, left : Node):
        if type(tokenList[tokenIndex]) not in operations:
            return tokenIndex, left
        operatorToken = tokenList[tokenIndex]
        tokenIndex = increment(tokenIndex, tokenList)
        tokenIndex, right = f(tokenList, tokenIndex)
        left = OperatorNode(left, operatorToken, right)
        return traverse(tokenIndex, left)

    return traverse(tokenIndex, left)

def parse(tokens: List[Token]) -> Node:
    """ Parse tokenlist
    Parse the passed tokenlist.

    Parameters:
        tokens (List): The list with tokens to parse.

    Returns:
        Node: The Root node of the AST.
    """
    return statements(tokens, 0)[1]
