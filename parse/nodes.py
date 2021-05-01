from lex import token
from typing import List, Union

class FunctionNode():
    def __init__(self, name : str, returnType : str, arguments : List[token.Token]):
        self.name = name
        self.returnType = returnType
        self.arguments = arguments
        self.codeSequence = []

class NumberNode():
    def __init__(self, token : token.Token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'

class VariableNode():
    def __init__(self, var_name, value = None):
    	self.var_name = var_name
    	self.value = value
    
    def __repr__(self):
        return f'{self.var_name}: {self.value}'

class OperatorNode():
    def __init__(self, left_node : 'Node', operator : 'Node', right_node : 'Node'):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operator}, {self.right_node})'

Node = Union[FunctionNode, NumberNode, OperatorNode, VariableNode]