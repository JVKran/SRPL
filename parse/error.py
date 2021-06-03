# SPDX-FileCopyrightText: © 2021 Jochem van Kranenburg <jochem.vankranenburg@outlook.com>
# PDX-License-Identifier: AGPL-3.0 License

from typing import List, Optional
from lex.token import Token

# increment :: Integer -> [Token] -> Token -> String | Nothing -> Integer
def increment(tokenIndex: int, tokenList: List[Token], expectedToken: Optional[Token] = None, message: Optional[str] = None) -> int:
    """ Increment tokenindex
    This function increments the token index to the next index and prints 
    an error when an unexpected token appears. 
    
    Parameters:
        tokenIndex (int): The current tokenindex that should be incremented.
        tokenList (List): The list with tokens that should be parsed.
        expectedToken (Optional[Token]): The type of the token that should be next.
        message (Optional[str]): The message to print when the next token isn't equal to the expected one.

    Returns:
        int: The (if possible) incremented tokenindex.
    """
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
