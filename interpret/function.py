from interpret.context import *
from interpret import interpreter

class Function:
    def __init__(self, name, codeSequence, argumentNames, context):
        self.name = name
        self.codeSequence = codeSequence
        self.argumentNames = argumentNames
        self.context = context

    def execute(self, arguments, parentContext):
        context = Context(self.name, parentContext)
        context.symbols = parentContext.symbols
        assert(len(arguments) == len(self.argumentNames))

        for i in range(len(arguments)):
            context.add_symbol(self.argumentNames[i], arguments[i])

        value = interpreter.visit(self.codeSequence, context)
        return value

    def __repr__(self):
        return f"<function {self.name}>"

