from lex.lexer import lex
from parse.parser import parse
from interpret.interpreter import *
from interpret.context import *
import sys

def file(context : Context):
    tokens = lex(None, sys.argv[1])
    ast = parse(tokens)
    result = visit(ast, context)
    
    print(str(result))

def shell(context : Context):
    while True:
        text = input("SRPL  > ")
        if text == "exit": exit(0)
        if text == "": continue

        tokens = lex([text], None)
        ast = parse(tokens)
        result = visit(ast, context)

        print("\t" + str(result))

if __name__ == '__main__':
    context = Context("<main>")
    try:
        if len(sys.argv) == 2:
            file(context)
        else:
            shell(context)
    except KeyboardInterrupt:
        print("Execution was interrupted!")
        exit(0)
