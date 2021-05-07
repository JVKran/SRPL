from parse.nodes import FunctionNode, IfNode, ReturnNode, VariableNode
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
            functionName: str = f'compile{type(node).__name__}'
            function = globals()[functionName]
            function(node)

    def __del__(self):
        self.file.write("\tpop \t{r4, r5, r6, pc}\n")
        self.file.close()

def compileIfNode(node : IfNode):
    print(node)
    print("IfNode has been compiled.")

def compileReturnNode(node : ReturnNode):
    print(node)
    print("ReturnNode has been compiled.")

def compileVariableNode(node : VariableNode):
    print(node)
    print("VariableNode has been compiled.")