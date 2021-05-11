from typing import Optional
from parse.nodes import Node

class Context():

    # __init__ :: String -> Context -> Nothing
    def __init__(self, name : str, parent : 'Context' = None):
        self.name = name
        self.parent = parent
        self.symbols = {}
        self.registers = ["r0", "r1", "r2", "r3", "r4", "r5", "r6"]

    # getSymbol :: String -> Node | Nothing
    def getSymbol(self, name : str) -> Optional[Node]:
        value: Optional[Node] = self.symbols.get(name, None)
        if value == None and self.parent != None:
            return self.parent.getSymbol(name)
        return value

    def getRegister(self, register: str = None):
        if register:
            return self.registers.remove(register)
        return self.registers.pop(0)

    def pop(self):
        self.registers = ["r0", "r1", "r2", "r3", "r4", "r5", "r6"]

    # __repr__ -> String
    def __repr__(self) -> str:
        return str(self.symbols)
