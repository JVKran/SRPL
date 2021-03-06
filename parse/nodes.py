# SPDX-FileCopyrightText: © 2021 Jochem van Kranenburg <jochem.vankranenburg@outlook.com>
# PDX-License-Identifier: AGPL-3.0 License

from lex.token import Token
from typing import List, Union, NamedTuple

class FunctionNode(NamedTuple):
    name: str
    arguments: List[Token]
    codeSequence: List['Node']

class CallNode(NamedTuple):
    nodeToCall: 'Node'
    argumentNodes: List['Node']

class ReturnNode(NamedTuple):
    nodeToReturn: 'Node'

class ListNode(NamedTuple):
    elementNodes: List['Node']

class NumberNode(NamedTuple):
    token: Token

    # __repr__ -> String
    def __repr__(self):
        return f'{self.token}'

class VariableNode(NamedTuple):
    var_name: str
    value: 'Node' = None
    
    # __repr__ -> String
    def __repr__(self):
        return f'{self.var_name}: {self.value}'

class OperatorNode(NamedTuple):
    left_node: 'Node'
    operator: 'OperatorNode'
    right_node: 'Node'

    # __repr__ -> String
    def __repr__(self):
        return f'({self.left_node}, {self.operator}, {self.right_node})'

class IfNode(NamedTuple):
    condition: 'Node'
    expression: 'Node'
    elseExpression: 'Node'

class WhileNode(NamedTuple):
    condition: 'Node'
    codeSequence: 'Node'

class ForNode(NamedTuple):
    varNameToken: 'Token'
    startNode: 'Node'
    endNode: 'Node'
    stepNode: 'Node'
    bodyNode: 'Node'

Node = Union[FunctionNode, CallNode, NumberNode, OperatorNode, VariableNode, IfNode, WhileNode, ListNode, ReturnNode]
