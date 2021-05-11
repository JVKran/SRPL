from parse.nodes import FunctionNode, IfNode, ReturnNode, VariableNode
from lex.token import *
from typing import List

class Compiler():

    def __init__(self, sourceFile : str, destinationFile : str, function : FunctionNode):
        self.function = function
        print("Compiling \'" + sourceFile + "\' to \'" + destinationFile + "\'.")
        requiredRegisters = max(1, len(function.arguments))
        print("This function requires", requiredRegisters, "registers!")

        self.file = open(destinationFile, "w")
        arguments: str = ("int, " * len(function.arguments))[:-2]       # Skip last ", "
        self.file.write(f'{function.name}({arguments}):\n')
        self.file.write("\tpush \t{r4, r5, r6, lr}\n")

    def compile(self):
        for i in range(len(self.function.codeSequence[0])):
            node = self.function.codeSequence[0][i]
            methodName: str = f'compile{type(node).__name__}'
            method = getattr(self, methodName)
            method(node)

    def __del__(self):
        self.file.write("\tpop \t{r4, r5, r6, pc}\n")
        self.file.close()

    def compileIfNode(self, node : IfNode):
        print(node)
        print("IfNode has been compiled.")

    def compileReturnNode(self, node : ReturnNode):
        print(node)
        print("ReturnNode has been compiled.")

    def compileVariableNode(self, node : VariableNode):
        operator = node.value[1]
        operatorName = ""
        if type(operator) == AddToken:
            operatorName = "adds"
        elif type(operator) == SubstractToken:
            operatorName = "subs"
        elif type(operator) == MultiplyToken:
            operatorName = "muls"
        self.file.write(f'\t{operatorName} \t{node.var_name}, {node.value[0].var_name.stringToParse}, {node.value[2].var_name.stringToParse}\n')
        print(node)
        print("VariableNode has been compiled.")