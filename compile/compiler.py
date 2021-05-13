from typing import List, Optional
from operator import is_not, add
from functools import partial, reduce
from itertools import chain
from copy import copy

from parse.nodes import *
from compile.context import Context
from compile.number import Number
from compile.function import Function
from lex.token import *

class Compiler():

    def __init__(self, sourceFile : str, destinationFile : str, function : FunctionNode):
        self.function = function
        print("Compiling \'" + sourceFile + "\' to \'" + destinationFile + "\'.")
        requiredRegisters = max(1, len(function.arguments))
        print("This function requires", requiredRegisters, "registers!")

        self.file = open(destinationFile, "w")
        self.file.write("\t.cpu cortex-m0\n")
        self.file.write("\t.text\n")
        self.file.write("\t.align 2\n")
        self.file.write(f"\t.global {function.name}\n\n")
        self.file.write(f'{function.name}:\n')
        self.file.write("\tpush \t{r4, r5, r6, lr}\n")

    def __del__(self):
        self.file.write("\tpop \t{r4, r5, r6, pc}\n")
        self.file.close()
    
    def compile(self, node : Node, context : Context):
        """ compile node and return result. """

    # compileOperatorNode :: OperatorNode -> Context -> Number
        def compileOperatorNode(node : OperatorNode, context : Context) -> Number:
            """ Execute operator on left and right node. """
            left = self.compile(node.left_node, context)
            right = self.compile(node.right_node, context)
            methodName = f'{type(node.operator).__name__}'.replace("Token", '')         # AddToken becomes Add, MultiplyToken becomes Multiply, etc.
            method = getattr(left, methodName)
            res = method(right, context, self.file)
            return res

        # compileNumbernode :: NumberNode -> Context -> Number
        def compileNumberNode(node : NumberNode, context : Context) -> Number:
            """ Create number from number node. """
            availableRegister = context.getRegister()
            number = Number(node.token.stringToParse, node.token.lineNumber, availableRegister)
            self.file.write(f"\tmovs\t{availableRegister}, #{number.value}\n")
            return number

        # compileVariableNode :: VariableNode -> Context -> Number
        def compileVariableNode(node : VariableNode, context : Context) -> Number:
            """ Get value of variable from symboltable or store value in table. """
            if node.value == None:
                variableName = node.var_name.stringToParse
                value = context.getSymbol(variableName)
            else:
                variableName = node.var_name
                value = self.compile(node.value, context)
                context.symbols[variableName] = value
            return value

        def compileIfNode(node : IfNode, context : Context) -> Optional[Number]:
            """ Execute expression of if statement when condition is met or exepression of else statement when provided. """
            conditionIsMet: Number = self.compile(node.condition, context)
            availableRegisters = copy(context.registers)            # Save registers since the condition is either true, or false.
            self.file.write(f"\tcmp \t{conditionIsMet.register}, #1\n")
            segment = context.getSegment()
            self.file.write(f"\tbne \t{segment}\n")                              # If condition isn't met; go to L2.
            resReg = context.registers[0]
            res = self.compile(node.expression, context)
            self.file.write("\tb\tend \n")
            self.file.write(f"{segment}:\n")
            context.registers = availableRegisters
            if node.elseExpression:
                self.compile(node.elseExpression, context)
                if(type(node.elseExpression) == CallNode):
                    self.file.write(f"\tmovs\t{resReg}, r0\n")                      # Inherent to the way SRPL deals with variables and return values.
            return res

        # compileWhileNode :: WhileNode -> Context -> Nothing
        def compileWhileNode(node : WhileNode, context : Context) -> None:
            """ Execute while loop until condition is no longer met. """
            self.file.write("loop:\n")
            conditionIsMet: Number = self.compile(node.condition, context)
            self.file.write(f"\tcmp \t{conditionIsMet.register}, #1\n")
            self.file.write(f"\tbne \tend\n")                              # If condition isn't met; go to L2.
            self.compile(node.codeSequence, context)
            self.file.write("\tb    \tloop\n")

        # compileFunctionNode :: FunctionNode -> Context -> Function
        def compileFunctionNode(node : FunctionNode, context : Context) -> Function:
            """ Create function from function definition and add it to symboltable. """
            functionValue = Function(node.name, node.codeSequence, node.arguments, context)
            context.symbols[node.name] = functionValue
            arguments = [Number(0, 0, context.getRegister()) for _ in range(len(node.arguments))]           # TODO: Make functional.
            codeSequence, context = functionValue.execute(arguments, context)
            return self.compile(codeSequence, context)

        def compileCallNode(node : FunctionNode, context : Context):
            arguments: List[Number] = []
            if node.argumentNodes != None:
                arguments = list(chain(*map(lambda node: [*arguments, self.compile(node, context)], node.argumentNodes)))
            self.file.write(f"\tbl  \t{node.nodeToCall.var_name.stringToParse}\n")

        # compileListNode :: ListNode -> Context -> Number | [Number]
        def compileListNode(node : ListNode, context : Context) -> Union[Number, List[Number]]:
            """ compile list node.
            This method might require some more explanation. This method determines
            the result of all nodes in the 'list'. These lists can occur since functions,
            but also files, are allowed to return 'flush' multiple values. So, for example,
            when a function returns once, there will only be one element in the returned list.
            But when a function doesn't return at all, the results of all nodes will be in 
            the list. Same goes for functions or files returning multiple times; a list
            will be returned.
            """
            returnNodes = map(lambda element: ReturnNode == type(element), node.elementNodes)
            returnPresent: Number = reduce(add, returnNodes, 0)                         # Are there any nodes that really flush something?
            
            def compileElement(elementNode):
                if not returnPresent:
                    return self.compile(elementNode, context)
                elif type(elementNode) == ReturnNode:
                    return self.compile(elementNode, context)
                self.compile(elementNode, context)

            elements: List[Number] = []
            elements = list(chain(*map(lambda node: [*elements, compileElement(node)], node.elementNodes)))
            elements = list(filter(partial(is_not, None), elements))            # Filter all None values. Note that None is equal to 0, so is_not is used.
            
            if len(elements) == 1:
                return elements[0]
            return elements

        # compileReturnNode :: ReturnNode -> Context -> Number | Nothing
        def compileReturnNode(node : ReturnNode, context : Context) -> Optional[Number]:
            """ Execute return statement. """
            if node.nodeToReturn:
                res = self.compile(node.nodeToReturn, context)
                self.file.write("end:\n")
                self.file.write(f"\tmovs\tr0, {res.register}\n")
                return res

        functionName: str = f'compile{type(node).__name__}'                       # Determine name of function to call.
        function = locals()[functionName]                                       # Get function with corresponding name.
        return function(node, context)
