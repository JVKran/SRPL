from typing import List, Tuple
from compile.context import Context
from compile import compiler
from compile.number import Number
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
        context = parentContext
        context.symbols = parentContext.symbols
        assert(len(arguments) == len(self.argumentNames))

        zippedArguments: List[Tuple[str, Number]] = list(zip(self.argumentNames, arguments))
        context.symbols.update(zippedArguments)

        return self.codeSequence, context

    # __repr__ -> String
    def __repr__(self):
        return f"<function {self.name}>"