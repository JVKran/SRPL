from lex import token
from lex import lexer

if __name__ == '__main__':
    lexer = lexer.Lexer("main.srpl")
    tokens = lexer.make_tokens()
    print(tokens)