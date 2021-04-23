from lex import token
from lex import lexer
import sys

if __name__ == '__main__':
    print(lexer.lex(sys.argv[1]))
    # lexer = lexer.Lexer(sys.argv[1])
    # tokens = lexer.make_tokens()
    # print(tokens)