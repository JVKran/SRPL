from typing import List, Optional
from lex.token import Token
from parse import parser

# increment :: Integer -> [Token] -> Token -> String | Nothing -> Integer
def increment(tokenIndex: int, tokenList: List[Token], expectedToken: Optional[Token] = None, message: Optional[str] = None) -> int:
    """ Increment to next index and print error when unexpected token appears. """
    if expectedToken and type(tokenList[tokenIndex]) != expectedToken:
        if message == None:     # Generate default error message.
            expected = str(expectedToken.__name__).replace("Token", '').lower()
            received = str(type(tokenList[tokenIndex]).__name__).replace("Token", '').lower()
            print("Expected " + expected + " instead of " + received + " at line " + str(tokenList[tokenIndex].lineNumber) + "!")
        else:
            print(message + " At line " + str(tokenList[tokenIndex].lineNumber) + ".")
    if tokenIndex >= len(tokenList) - 1:
        return tokenIndex
    return tokenIndex + 1
