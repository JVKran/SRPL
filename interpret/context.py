
class Context():
    def __init__(self, name, parent = None):
        self.name = name
        self.parent = parent
        self.symbols = {}

    def add_symbol(self, name, value):
        self.symbols[name] = value
        return self

    def get_symbol(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent.symbols != None:
            return self.parent.get_symbol(name)
        return value
