from lex import token, lexer
from parse import parser
import sys

if __name__ == '__main__':
    tokens = lexer.lex(sys.argv[1])
    parser.parse(tokens)