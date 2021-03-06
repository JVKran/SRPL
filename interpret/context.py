# SPDX-FileCopyrightText: © 2021 Jochem van Kranenburg <jochem.vankranenburg@outlook.com>
# PDX-License-Identifier: AGPL-3.0 License

from typing import Optional
from parse.nodes import Node

class Context():

    # __init__ :: String -> Context -> Nothing
    def __init__(self, name : str, parent : 'Context' = None):
        self.name = name
        self.parent = parent
        self.symbols = {}

        # Only used by compiler.
        self.registers = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7"]
        self.labels = [".L2", ".L4", ".L6", ".L8", ".L10"]

    # getSymbol :: String -> Node | Nothing
    def getSymbol(self, name : str) -> Optional[Node]:
        value: Optional[Node] = self.symbols.get(name, None)
        if value == None and self.parent != None:
            return self.parent.getSymbol(name)
        return value

    # __repr__ -> String
    def __repr__(self) -> str:
        return str(self.symbols)
