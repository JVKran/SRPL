from typing import Union

class Number():

    def __init__(self, value : Union[int, float]):
        self.value = value

    def Add(self, other : 'Number') -> 'Number':
        return Number(self.value + other.value)

    def Substract(self, other : 'Number') -> 'Number':
        return Number(self.value - other.value)

    def Multiply(self, other : 'Number') -> 'Number':
        return Number(self.value * other.value)

    def Divide(self, other : 'Number') -> 'Number':
        return Number(self.value / other.value)

    def Equality(self, other : 'Number') -> 'Number':
        return Number(int(self.value == other.value))
    
    def NonEquality(self, other : 'Number') -> 'Number':
        return Number(int(self.value != other.value))

    def Less(self, other : 'Number') -> 'Number':
        return Number(int(self.value < other.value))

    def Greater(self, other : 'Number') -> 'Number':
        return Number(int(self.value > other.value))

    def LessEqual(self, other : 'Number') -> 'Number':
        return Number(int(self.value <= other.value))

    def GreaterEqual(self, other : 'Number') -> 'Number':
        return Number(int(self.value >= other.value))

    def And(self, other : 'Number') -> 'Number':
        return Number(int(self.value and other.value))

    def Or(self, other : 'Number') -> 'Number':
        return Number(int(self.value or other.value))

    def setLineNumber(self, number : int):
        self.lineNumber = number

    def __bool__(self):
        return self.value != 0

    def __repr__(self) -> str:
        return str(self.value)
