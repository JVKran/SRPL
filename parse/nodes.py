from lex import token
from typing import List, Union

class FunctionNode():
    def __init__(self, name : str, arguments : List[token.Token], codeSequence):
        self.name = name
        self.arguments = arguments
        self.codeSequence = codeSequence

class CallNode:
	def __init__(self, node_to_call, arg_nodes):
		self.node_to_call = node_to_call
		self.arg_nodes = arg_nodes

class ListNode():
  def __init__(self, element_nodes):
    self.element_nodes = element_nodes

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

class IfNode():
    def __init__(self, condition, expression):
        self.condition = condition
        self.expression = expression

class WhileNode():
    def __init__(self, condition, codeSequence):
        self.condition = condition
        self.codeSequence = codeSequence

Node = Union[FunctionNode, CallNode, NumberNode, OperatorNode, VariableNode, IfNode, WhileNode, ListNode]