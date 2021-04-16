from lex import token

if __name__ == '__main__':
    testToken = token.Token("is", 5)
    print(type(testToken))
    print(testToken.lineNumber)