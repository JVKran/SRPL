from typing import Union

class Number():

    def __init__(self, value : Union[int, float], lineNumber : int):
        self.value = value
        self.lineNumber = lineNumber

    def Add(self, other : 'Number') -> 'Number':
        return Number(self.value + other.value, self.lineNumber)

    def Substract(self, other : 'Number') -> 'Number':
        return Number(self.value - other.value, self.lineNumber)

    def Multiply(self, other : 'Number') -> 'Number':
        return Number(self.value * other.value, self.lineNumber)

    def Divide(self, other : 'Number') -> 'Number':
        return Number(self.value / other.value, self.lineNumber)

    def Equality(self, other : 'Number') -> 'Number':
        return Number(int(self.value == other.value), self.lineNumber)
    
    def NonEquality(self, other : 'Number') -> 'Number':
        return Number(int(self.value != other.value), self.lineNumber)

    def Less(self, other : 'Number') -> 'Number':
        return Number(int(self.value < other.value), self.lineNumber)

    def Greater(self, other : 'Number') -> 'Number':
        return Number(int(self.value > other.value), self.lineNumber)

    def LessEqual(self, other : 'Number') -> 'Number':
        return Number(int(self.value <= other.value), self.lineNumber)

    def GreaterEqual(self, other : 'Number') -> 'Number':
        return Number(int(self.value >= other.value), self.lineNumber)

    def And(self, other : 'Number') -> 'Number':
        return Number(int(self.value and other.value), self.lineNumber)

    def Or(self, other : 'Number') -> 'Number':
        return Number(int(self.value or other.value), self.lineNumber)

    def __bool__(self) -> bool:
        return self.value != 0

    def __repr__(self) -> str:
        return str(self.value)
