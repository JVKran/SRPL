from parse import parser

def increment(tokenIndex, tokenList, expectedToken, message = None) -> int:
    if expectedToken and type(tokenList[tokenIndex]) != expectedToken:
        if message == None:     # Generate default error message.
            expected = str(expectedToken.__name__).replace("Token", '').lower()
            received = str(type(tokenList[tokenIndex]).__name__).replace("Token", '').lower()
            print("Expected " + expected + " instead of " + received + " at line " + str(tokenList[tokenIndex].lineNumber) + "!")
        else:
            print(message + " At line " + str(tokenList[tokenIndex].lineNumber) + ".")
    tokenIndex = parser.incrementTokenIndex(tokenIndex, len(tokenList))
    return tokenIndex
