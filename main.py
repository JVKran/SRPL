from lex import token

if __name__ == '__main__':
    testToken = token.Token("5", 5)
    print(type(testToken))
    print("Variable value:", testToken.name)
    print("At linenumber:", testToken.lineNumber)