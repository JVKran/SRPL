from parse.nodes import FunctionNode
from typing import List

class Compiler():

    def __init__(self, sourceFile : str, destinationFile : str, function : FunctionNode):
        print("Compiling \'" + sourceFile + "\' to \'" + destinationFile + "\'.")
        requiredRegisters = max(1, len(function.arguments))
        print("This function requires", requiredRegisters, "registers!")

        self.file = open(destinationFile, "w")
        arguments: str = ("int, " * len(function.arguments))[:-2]       # Skip last ", "
        self.file.write(f'{function.name}({arguments}):\n')
        self.file.write("\tpush \t{r4, r5, r6, lr}\n")

    def __del__(self):
        self.file.write("\tpop \t{r4, r5, r6, pc}\n")
        self.file.close()