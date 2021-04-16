from lex import token

if __name__ == '__main__':
    testToken = token.Token("var", 5)
    print(type(testToken))
    print("Variable value:", testToken.stringToParse)
    print("At linenumber:", testToken.lineNumber)