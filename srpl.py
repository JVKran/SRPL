from lex.lexer import lex
from parse.parser import parse
from interpret.interpreter import *
from interpret.context import *
from compile.compiler import *
import sys

# file :: Context -> String
def file(context : Context) -> str:
    """ Lex, parse and interpret file with name of first commandline argument. """
    tokens: List[Token] = lex(None, sys.argv[1])
    ast: Node = parse(tokens)
    result: Union[List[Number], Number] = visit(ast, context)
    return str(result)

# shell :: Context -> Nothing
def shell(context : Context):
    """ Read, lex, parse and interpret shell commands until user exits. """
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
        if len(sys.argv) == 2:          # If filename has been passed as argument.
            print(file(context))
        elif len(sys.argv) == 3:          # If filename has been passed as argument.
            tokens: List[Token] = lex(None, sys.argv[1])
            ast: Node = parse(tokens)
            compiler = Compiler(sys.argv[1], sys.argv[2], ast[0][0])
            compiler.compile()
        else:
            shell(context)
    except KeyboardInterrupt:
        print("Execution was interrupted!")
        exit(0)
    except RecursionError:
        print("Maximum recursion depth exceeded!")
        exit(1)
    except FileNotFoundError:
        print("File \'" + sys.argv[1] + "\' could't be found.")
        exit(1)
