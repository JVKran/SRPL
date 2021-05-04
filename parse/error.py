from parse import parser
from typing import NamedTuple, Optional

def increment(tokenIndex, tokenList, expectedToken, message = None) -> int:
    if expectedToken and type(tokenList[tokenIndex]) != expectedToken:
        if message == None:     # Generate default error message.
            print("Expected " + str(expectedToken) + " instead of " + str(type(tokenList[tokenIndex])) + " at line " + str(tokenList[tokenIndex].lineNumber) + "!")
        else:
            print(message + " At line " + str(tokenList[tokenIndex].lineNumber) + ".")
    tokenIndex = parser.incrementTokenIndex(tokenIndex, len(tokenList))
    return tokenIndex
