
class Context():
    def __init__(self, name, parent = None):
        self.name = name
        self.parent = parent
        self.symbols = {}

    def getSymbol(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent.symbols != None:
            return self.parent.getSymbol(name)
        return value

    def __repr__(self) -> str:
        return str(self.symbols)
