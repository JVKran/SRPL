from lex import token
from lex import lexer
import sys

if __name__ == '__main__':
    tokens = lexer.lex(sys.argv[1])
    print(tokens)