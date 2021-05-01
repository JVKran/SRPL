from typing import Union

class Number():

    def __init__(self, value : Union[int, float]):
        self.value = value

    def add(self, other : 'Number') -> 'Number':
        return Number(self.value + other.value)

    def sub(self, other : 'Number') -> 'Number':
        return Number(self.value - other.value)

    def mul(self, other : 'Number') -> 'Number':
        return Number(self.value * other.value)

    def div(self, other : 'Number') -> 'Number':
        return Number(self.value / other.value)

    def eq(self, other : 'Number') -> 'Number':
        return Number(int(self.value == other.value))
    
    def ne(self, other : 'Number') -> 'Number':
        return Number(int(self.value != other.value))

    def lt(self, other : 'Number') -> 'Number':
        return Number(int(self.value < other.value))

    def gt(self, other : 'Number') -> 'Number':
        return Number(int(self.value > other.value))

    def lte(self, other : 'Number') -> 'Number':
        return Number(int(self.value <= other.value))

    def gte(self, other : 'Number') -> 'Number':
        return Number(int(self.value >= other.value))

    def anded_by(self, other : 'Number') -> 'Number':
        return Number(int(self.value and other.value))

    def ored_by(self, other : 'Number') -> 'Number':
        return Number(int(self.value or other.value))

    def setLineNumber(self, number : int):
        self.lineNumber = number

    def __bool__(self):
        return self.value != 0

    def __repr__(self) -> str:
        return str(self.value)
