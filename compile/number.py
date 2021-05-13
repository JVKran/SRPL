from typing import Union
from compile.context import Context
import interpret

class Number():

    # __init__ :: Integer | Float -> Integer -> Nothing
    def __init__(self, value : Union[int, float], lineNumber : int, register : str):
        self.value = value
        self.lineNumber = lineNumber
        self.register = register

    # Add :: Number -> Number
    def Add(self, other : 'Number', context: Context) -> 'Number':
        print(f'\tadd\t{self.register}, {other.register}')
        return Number(self.value + other.value, self.lineNumber, self.register)

    # Substract :: Number -> Number
    def Substract(self, other : 'Number', context: Context) -> 'Number':
        print(f'\tsub\t{self.register}, {other.register}')
        return Number(self.value - other.value, self.lineNumber, self.register)

    # Multiply :: Number -> Number
    def Multiply(self, other : 'Number', context: Context) -> 'Number':
        print(f'\tmuls\t{self.register}, {self.register}, {other.register}')            # Multiply self with other and store in self.
        return Number(self.value * other.value, self.lineNumber, self.register)

    # Divide :: Number -> Number
    def Divide(self, other : 'Number', context: Context) -> 'Number':
        # TODO: Make sure numbers to divide are in r0 and r1.
        print("\tbl\t__aeabi_idiv")
        return Number(self.value / other.value, self.lineNumber, self.register)

    # Equality :: Number -> Number
    def Equality(self, other : 'Number', context: Context) -> 'Number':
        scratchRegister = context.getRegister()
        print(f"\tsub\t{self.register}, {other.register}, {self.register}")
        print(f"\tneg\t{scratchRegister}, {self.register}")           # TODO: Request register from context.
        print(f"\tadc\t{scratchRegister}, {scratchRegister}, {self.register}")
        return Number(int(self.value == other.value), self.lineNumber, scratchRegister) # Scratchregister contains result.

    # NonEquality :: Number -> Number    
    def NonEquality(self, other : 'Number', context: Context) -> 'Number':
        scratchRegister = context.getRegister()
        print(f"\tsub\t{scratchRegister}, {other.register}, {self.register}")
        print(f"\tsub\t{self.register}, {scratchRegister}, #1")
        print(f"\tsdc\t{scratchRegister}, {scratchRegister}, {self.register}")
        return Number(int(self.value != other.value), self.lineNumber, self.register)

    # Less :: Number -> Number
    def Less(self, other : 'Number', context: Context) -> 'Number':
        scratchRegister = context.getRegister()
        print(f"\tmovs\t{scratchRegister}, #1")
        print(f"\tcmp\t{self.register}, {other.register}")
        print("\tblt\t.L2")
        print(f"\tmovs\t{scratchRegister}, #0")
        print(".L2:")
        print(f"\tmovs\t{self.register}, {scratchRegister}")
        return Number(int(self.value < other.value), self.lineNumber, self.register)

    # Greater :: Number -> Number
    def Greater(self, other : 'Number', context: Context) -> 'Number':
        scratchRegister = context.getRegister()
        print(f"\tmovs\t{scratchRegister}, #1")
        print(f"\tcmp\t{self.register}, {other.register}")
        print("\tbgt\t.L2")
        print(f"\tmovs\t{scratchRegister}, #0")
        print(".L2:")
        print(f"\tmovs\t{self.register}, {scratchRegister}")
        return Number(int(self.value > other.value), self.lineNumber, self.register)

    # LessEqual :: Number -> Number
    def LessEqual(self, other : 'Number', context: Context) -> 'Number':
        print(f"\tlsrs\t{self.register}, {self.register}, #31")
        print(f"\tasrs\tr2, {other.register}, #31")
        print(f"\tcmp\t{other.register}, r3")
        print(f"\tadcs\t{self.register}, {self.register}, r2")
        return Number(int(self.value <= other.value), self.lineNumber, self.register)

    # GreaterEqual :: Number -> Number
    def GreaterEqual(self, other : 'Number', context: Context) -> 'Number':
        print(f"\tmovs\tr3, {self.register}")
        print(f"\tasrs\t{self.register}, {self.register}, #31")
        print(f"\tlsrs\tr2, {other.register}, #31")
        print(f"\tcmp\tr3, {other.register}")
        print(f"\tadcs\t{self.register}, {self.register}, r2")
        return Number(int(self.value >= other.value), self.lineNumber, self.register)

    # And :: Number -> Number
    def And(self, other : 'Number', context: Context) -> 'Number':
        print(f"\tmovs    r3, r0")
        print(f"\tmovs    r0, #0")
        print(f"\tcmp     r3, #0")
        print(f"\tbeq     .L2")
        print(f"\tsub    r0, r1, #1")
        print(f"\tsbcs    r1, r1, r0")
        print(f"\tuxtb    r0, r1")
        print(f".L2:")
        return Number(int(self.value and other.value), self.lineNumber, self.register)

    # Or :: Number -> Number
    def Or(self, other : 'Number', context: Context) -> 'Number':
        print(f"\torrs\t{self.register}, {other.register}")
        print(f"\tsub\t{other.register}, {self.register}, #1")
        print(f"\tsbcs\t{self.register}, {self.register}, {other.register}")
        return Number(int(self.value or other.value), self.lineNumber, self.register)

    # __bool__ -> Boolean
    def __bool__(self) -> bool:
        return self.value != 0

    # __repr__ -> String
    def __repr__(self) -> str:
        return str(self.value)
