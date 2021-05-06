from lex.token import Token
from typing import List, Union, NamedTuple

class FunctionNode(NamedTuple):
    name: str
    arguments: List[Token]
    codeSequence: List['Node']

class CallNode(NamedTuple):
    node_to_call: 'Node'
    arg_nodes: List['Node']

class ReturnNode(NamedTuple):
    nodeToReturn: 'Node'

class ListNode(NamedTuple):
    element_nodes: List['Node']

class NumberNode(NamedTuple):
    token: Token

    def __repr__(self):
        return f'{self.token}'

class VariableNode(NamedTuple):
    var_name: str
    value: 'Node' = None
    
    def __repr__(self):
        return f'{self.var_name}: {self.value}'

class OperatorNode(NamedTuple):
    left_node: 'Node'
    operator: 'OperatorNode'
    right_node: 'Node'

    def __repr__(self):
        return f'({self.left_node}, {self.operator}, {self.right_node})'

class IfNode(NamedTuple):
    condition: 'Node'
    expression: 'Node'
    elseExpression: 'Node'

class WhileNode(NamedTuple):
    condition: 'Node'
    codeSequence: 'Node'

Node = Union[FunctionNode, CallNode, NumberNode, OperatorNode, VariableNode, IfNode, WhileNode, ListNode, ReturnNode]
