# SPDX-FileCopyrightText: © 2021 Jochem van Kranenburg <jochem.vankranenburg@outlook.com>
# PDX-License-Identifier: AGPL-3.0 License

from typing import List, Tuple
from interpret.context import Context
from interpret import interpreter
from interpret.number import Number
from parse.nodes import ListNode

class Function:

    # __init__ :: String -> ListNode -> [String] -> Context -> Nothing
    def __init__(self, name : str, codeSequence : ListNode, argumentNames : List[str], context : Context):
        self.name = name
        self.codeSequence = codeSequence
        self.argumentNames = argumentNames
        self.context = context

    # execute :: [Number] -> Context -> Number
    def execute(self, arguments : List[Number], parentContext : Context) -> Number:
        """ Execute function
        Execute the function by updating the values of all symbols in the symboltable. Note that
        this symboltable also contains the symbols of the parent. Afther these symbols and their
        corresponding values have been added to the table, the interpreter is ready to visit the
        node with which the function starts.

        Parameter:
            arguments (List[Number]): The list with arguments to pass to the function.
            parentContext (Context): The context of which the symbols should be updated.

        Returns:
            Number: The result of execution of the function.
        """
        context = Context(self.name, parentContext)
        context.symbols = parentContext.symbols
        assert(len(arguments) == len(self.argumentNames))

        zippedArguments: List[Tuple[str, Number]] = list(zip(self.argumentNames, arguments))
        context.symbols.update(zippedArguments)

        return interpreter.visit(self.codeSequence, context)

    # __repr__ -> String
    def __repr__(self):
        return f"<function {self.name}>"
