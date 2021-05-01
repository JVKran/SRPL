from lex import token, lexer
from parse import parser
from interpret import interpreter
import sys

def file():
    tokens = lexer.lex(None, sys.argv[1])
    print("TOKENS:", tokens)

    ast = parser.parse(tokens)
    print("AST:", ast)

    result = interpreter.visit(ast)
    print(str(result))

def shell():
    try:
        while True:
            text = input("SRPL > ")
            if text == "exit": exit()

            tokens = lexer.lex([text], None)
            print("\tTOKENS:", tokens)

            ast = parser.parse(tokens)
            print("\tAST:", ast)

            result = interpreter.visit(ast)
            print("\t" + str(result))
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file()
    else:
        shell()