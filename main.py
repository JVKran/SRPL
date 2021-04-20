from lex import token
from lex import lexer

if __name__ == '__main__':
    testToken = token.Token("is", 5)
    print("Type", type(testToken))
    print("Value", testToken.stringToParse, end=" ")
    print("at linenumber", testToken.lineNumber)

    lexer = lexer.Lexer("condition is 5 is less than 4.1 ")
    lexer.make_tokens()