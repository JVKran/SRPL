from lex import token, lexer
from parse import parser
import sys

def file():
    tokens = lexer.lex(None, sys.argv[1])
    print("Tokens:", tokens)

    ast = parser.parse(tokens)
    print("Abstract syntax tree:", ast)

def shell():
    while True:
        text = input("SRPL > ")
        if text == "exit": exit()

        tokens = lexer.lex([text], None)
        print("Tokens:", tokens)

        ast = parser.parse(tokens)
        print("Abstract syntax tree:", ast)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file()
    else:
        shell()