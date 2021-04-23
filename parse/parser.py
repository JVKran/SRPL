from lex import token
from typing import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

class FunctionNode():

    def __init__(self, name : str, returnType : str, arguments : List[token.Token]):
        self.name = name
        self.returnType = returnType
        self.arguments = arguments
        self.codeSequence = []

def parse(tokens: List[token.Token]):
    print(tokens)