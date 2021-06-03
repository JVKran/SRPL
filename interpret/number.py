# SPDX-FileCopyrightText: © 2021 Jochem van Kranenburg <jochem.vankranenburg@outlook.com>
# PDX-License-Identifier: AGPL-3.0 License

from typing import Union

class Number():

    # __init__ :: Integer | Float -> Integer -> Nothing
    def __init__(self, value : Union[int, float], lineNumber : int):
        self.value = value
        self.lineNumber = lineNumber

    # Add :: Number -> Number
    def Add(self, other : 'Number') -> 'Number':
        return Number(self.value + other.value, self.lineNumber)

    # Substract :: Number -> Number
    def Substract(self, other : 'Number') -> 'Number':
        return Number(self.value - other.value, self.lineNumber)

    # Multiply :: Number -> Number
    def Multiply(self, other : 'Number') -> 'Number':
        return Number(self.value * other.value, self.lineNumber)

    # Divide :: Number -> Number
    def Divide(self, other : 'Number') -> 'Number':
        return Number(self.value / other.value, self.lineNumber)

    # Equality :: Number -> Number
    def Equality(self, other : 'Number') -> 'Number':
        return Number(int(self.value == other.value), self.lineNumber)

    # NonEquality :: Number -> Number    
    def NonEquality(self, other : 'Number') -> 'Number':
        return Number(int(self.value != other.value), self.lineNumber)

    # Less :: Number -> Number
    def Less(self, other : 'Number') -> 'Number':
        return Number(int(self.value < other.value), self.lineNumber)

    # Greater :: Number -> Number
    def Greater(self, other : 'Number') -> 'Number':
        return Number(int(self.value > other.value), self.lineNumber)

    # LessEqual :: Number -> Number
    def LessEqual(self, other : 'Number') -> 'Number':
        return Number(int(self.value <= other.value), self.lineNumber)

    # GreaterEqual :: Number -> Number
    def GreaterEqual(self, other : 'Number') -> 'Number':
        return Number(int(self.value >= other.value), self.lineNumber)

    # And :: Number -> Number
    def And(self, other : 'Number') -> 'Number':
        return Number(int(self.value and other.value), self.lineNumber)

    # Or :: Number -> Number
    def Or(self, other : 'Number') -> 'Number':
        return Number(int(self.value or other.value), self.lineNumber)

    # __bool__ -> Boolean
    def __bool__(self) -> bool:
        return self.value != 0

    # __repr__ -> String
    def __repr__(self) -> str:
        return str(self.value)
