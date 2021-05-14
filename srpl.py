import sys
from typing import List, Union

from lex.lexer import lex
from parse.parser import parse
from interpret.interpreter import visit
from compile.compiler import Compiler

import interpret
import compile
from interpret.number import Number
from parse.nodes import Node
from lex.token import Token

# file :: Context -> String
def interpretFile(filename: str) -> str:
    """ Interpret file
    This function is used for reading, lexing, parsing and finally interpreting
    an SRPL sourcefile.

    Parameters:
        filename (str): The name of the file to read, lex, parse and interpret.

    Returns:
        result (str): A textual representation of the result.
    """
    context = interpret.context.Context(f"<{filename}>")
    tokens: List[Token] = lex(None, filename)
    ast: Node = parse(tokens)
    result: Union[List[Number], Number] = visit(ast, context)
    return str(result)

# compileFiles -> Nothing
def compileFiles():
    """ Compile files 
    This function recurively traverses all files in all subdirectories in search of
    SRPL sourcefiles. These are then read, lexed, parsed and finally compiled into
    an assembly file.
    """
    import os
    for directory, subdirectory, files in os.walk("."):
        for file in files:
            if file.endswith(".srpl") and not file.startswith("main"):
                targetFileName = directory + "\\" + file.replace(".srpl", ".asm")
                sourceFileName = directory + "\\" + file
                os.system(f'python srpl.py {sourceFileName} {targetFileName}')

# compileFile :: String -> String -> Nothing
def compileFile(srplSource: str, asmTarget: str):
    """ Compile file
    This function can be called to compile one single SRPL sourcefile to an assembly
    targetfile. Note that only the first node is compiled and that only the compilation
    of functions is 'officially' supported.

    Parameters:
        sprlSource (str): The path to the SRPL sourcefile to compile.
        asmTarget (str): The path to the assembly targetfile into which the sourcefile
                            should be compiled.
    """
    tokens: List[Token] = lex(None, srplSource)
    ast: Node = parse(tokens)
    nodeToCompile = ast[0][0]                     # Only the first node will be visited.
    compiler = Compiler(srplSource, asmTarget, nodeToCompile)
    compiler.compile(ast)

# shell -> Nothing
def shell():
    """ SRPL Shell
    This function starts the shell and keeps it running until the user decides to exit
    by pressing CTRL+C or typing exit. Furterhmore, the user can recursively compile all
    SRPL sourcefiles by executing compile.
    """
    context = interpret.context.Context("<shell>")
    while True:
        text = input("SRPL  > ")
        if text == "exit": exit(0)
        if text == "": continue
        if text == "compile": 
            compileFiles()
            continue

        tokens = lex([text], None)
        ast = parse(tokens)
        result = visit(ast, context)
        print("\t" + str(result))

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:              # If filename has been passed as argument.
            print(interpretFile(sys.argv[1]))
        elif len(sys.argv) == 3:             # If SRPL sourcefile and assembly targetfile have been passed as argument.
            compileFile(sys.argv[1], sys.argv[2])
        else:
            shell()
    except KeyboardInterrupt:
        print("Execution was interrupted!")
        exit(0)
    except RecursionError:
        print("Maximum recursion depth exceeded!")
    except FileNotFoundError:
        print("File \'" + sys.argv[1] + "\' could't be found.")
    exit(1)
