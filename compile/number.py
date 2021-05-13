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
    def Add(self, other : 'Number', context: Context, file) -> 'Number':
        file.write(f'\tadd \t{self.register}, {other.register}\n')
        return Number(self.value + other.value, self.lineNumber, self.register)

    # Substract :: Number -> Number
    def Substract(self, other : 'Number', context: Context, file) -> 'Number':
        file.write(f'\tsub \t{self.register}, {other.register}\n')
        return Number(self.value - other.value, self.lineNumber, self.register)

    # Multiply :: Number -> Number
    def Multiply(self, other : 'Number', context: Context, file) -> 'Number':
        file.write(f'\tmuls\t{self.register}, {self.register}, {other.register}\n')            # Multiply self with other and store in self.
        return Number(self.value * other.value, self.lineNumber, self.register)

    # Divide :: Number -> Number
    def Divide(self, other : 'Number', context: Context, file) -> 'Number':
        # TODO: Make sure numbers to divide are in r0 and r1.
        file.write("\tbl  \t__aeabi_idiv\n")
        return Number(self.value / other.value, self.lineNumber, self.register)

    # Equality :: Number -> Number
    def Equality(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.getRegister()
        tempRegister = context.getRegister()                        # Used since we don't want the original register to change.
        file.write(f"\tsub \t{tempRegister}, {other.register}, {self.register}\n")
        file.write(f"\tneg \t{scratchRegister}, {tempRegister}\n")           # TODO: Request register from context.
        file.write(f"\tadc \t{scratchRegister}, {scratchRegister}, {tempRegister}\n")
        return Number(int(self.value == other.value), self.lineNumber, scratchRegister) # Scratchregister contains result.

    # NonEquality :: Number -> Number    
    def NonEquality(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.getRegister()
        tempRegister = context.getRegister()                            # TODO: Free temp register.
        file.write(f"\tsub \t{tempRegister}, {other.register}, {self.register}\n")
        file.write(f"\tsub \t{scratchRegister}, {tempRegister}, #1\n")
        file.write(f"\tsbc \t{scratchRegister}, {scratchRegister}, {scratchRegister}\n")
        return Number(int(self.value != other.value), self.lineNumber, scratchRegister)

    # Less :: Number -> Number
    def Less(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.getRegister()
        file.write(f"\tmov \t{scratchRegister}, #1\n")
        file.write(f"\tcmp \t{self.register}, {other.register}\n")
        file.write("\tblt \t.L2\n")
        file.write(f"\tmovs\t{scratchRegister}, #0\n")
        file.write(".L2:\n")
        file.write(f"\tmovs\t{self.register}, {scratchRegister}\n")
        return Number(int(self.value < other.value), self.lineNumber, self.register)

    # Greater :: Number -> Number
    def Greater(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.getRegister()
        file.write(f"\tmovs\t{scratchRegister}, #1\n")
        file.write(f"\tcmp \t{self.register}, {other.register}\n")
        file.write("\tbgt \t.L2\n")
        file.write(f"\tmovs\t{scratchRegister}, #0\n")
        file.write(".L2:\n")
        file.write(f"\tmovs\t{self.register}, {scratchRegister}\n")
        return Number(int(self.value > other.value), self.lineNumber, self.register)

    # LessEqual :: Number -> Number
    def LessEqual(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.getRegister()
        tempRegister = context.getRegister()
        file.write(f"\tlsr \t{scratchRegister}, {self.register}, #31\n")
        file.write(f"\tasr \t{tempRegister}, {other.register}, #31\n")
        file.write(f"\tcmp \t{self.register}, {other.register}\n")
        file.write(f"\tadc \t{scratchRegister}, {scratchRegister}, {tempRegister}\n")
        return Number(int(self.value <= other.value), self.lineNumber, scratchRegister)

    # GreaterEqual :: Number -> Number
    def GreaterEqual(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.getRegister()
        otherRegister = context.getRegister()
        file.write(f"\tasr \t{scratchRegister}, {self.register}, #31\n")
        file.write(f"\tlsr \t{otherRegister}, {other.register}, #31\n")
        file.write(f"\tcmp \t{self.register}, {other.register}\n")
        file.write(f"\tadc \t{scratchRegister}, {scratchRegister}, {otherRegister}\n")
        return Number(int(self.value >= other.value), self.lineNumber, scratchRegister)

    # And :: Number -> Number
    def And(self, other : 'Number', context: Context, file) -> 'Number':
        file.write(f"\tmovs    r3, r0\n")
        file.write(f"\tmovs    r0, #0\n")
        file.write(f"\tcmp     r3, #0\n")
        file.write(f"\tbeq     .L2\n")
        file.write(f"\tsub    r0, r1, #1\n")
        file.write(f"\tsbcs    r1, r1, r0\n")
        file.write(f"\tuxtb    r0, r1\n")
        file.write(f".L2:\n")
        return Number(int(self.value and other.value), self.lineNumber, self.register)

    # Or :: Number -> Number
    def Or(self, other : 'Number', context: Context, file) -> 'Number':
        file.write(f"\torrs\t{self.register}, {other.register}\n")
        file.write(f"\tsub\t{other.register}, {self.register}, #1\n")
        file.write(f"\tsbcs\t{self.register}, {self.register}, {other.register}\n")
        return Number(int(self.value or other.value), self.lineNumber, self.register)

    # __bool__ -> Boolean
    def __bool__(self) -> bool:
        return self.value != 0

    # __repr__ -> String
    def __repr__(self) -> str:
        return str(self.value)
