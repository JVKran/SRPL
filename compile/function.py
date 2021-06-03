# SPDX-FileCopyrightText: © 2021 Jochem van Kranenburg <jochem.vankranenburg@outlook.com>
# PDX-License-Identifier: AGPL-3.0 License

from typing import List, Tuple
from interpret.context import Context
from compile.number import Number
from parse.nodes import ListNode

class Function:

    # __init__ :: String -> ListNode -> [String] -> Context -> Nothing
    def __init__(self, name : str, codeSequence : ListNode, argumentNames : List[str], context : Context):
        self.name = name
        self.codeSequence = codeSequence
        self.argumentNames = argumentNames
        self.context = context

    # compile :: [Number] -> Context -> Number
    def compile(self, arguments : List[Number], context : Context) -> Tuple[ListNode, Context]:
        """ Compile function
        Funny thing here is that nothing is executed nor compiled; this is up to the
        compiler. We only add the arguments to the symboltable and return the code-
        sequence that has to be compiled.

        Parameter:
            arguments (List[Number]): The list with arguments to pass to the function.
            parentContext (Context): The context of which the symbols should be updated.

        Returns:
            codeSequence: The code sequence for the compiler to compile.
            context: The context to use for compilation.
        """
        assert(len(arguments) == len(self.argumentNames))
        zippedArguments: List[Tuple[str, Number]] = list(zip(self.argumentNames, arguments))
        context.symbols.update(zippedArguments)
        return self.codeSequence, context

    # __repr__ -> String
    def __repr__(self):
        return f"<function {self.name}>"
