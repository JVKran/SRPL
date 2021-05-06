from interpret.context import Context
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

        zippedArguments = list(zip(self.argumentNames, arguments))
        context.symbols.update(zippedArguments)

        value = interpreter.visit(self.codeSequence, context)
        return value

    def __repr__(self):
        return f"<function {self.name}>"
