from lex import token, lexer
from parse import parser
from interpret.interpreter import *
from interpret.context import *
import sys

def file():
    tokens = lexer.lex(None, sys.argv[1])
    ast = parser.parse(tokens)
    context = Context("<main>")
    result = visit(ast, context)
    
    print(str(result))

def shell():
    try:
        context = Context("<main>")
        while True:
            text = input("SRPL > ")
            if text == "exit": exit()
            if text == "": continue

            tokens = lexer.lex([text], None)
            ast = parser.parse(tokens)
            result = visit(ast, context)

            if len(result) > 1: print("\t" + str(result))
            else: print("\t" + str(result[0]))
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file()
    else:
        shell()