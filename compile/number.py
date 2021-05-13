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
        file.write(f'\tmul\t{self.register}, {self.register}, {other.register}\n')            # Multiply self with other and store in self.
        return Number(self.value * other.value, self.lineNumber, self.register)

    # Divide :: Number -> Number
    def Divide(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.registers.pop(0)
        file.write("\tpush\t {r0, r1}\n")
        # Move values to r0 and r1.
        file.write(f"\tmov \tr0, {self.register}\n")
        file.write(f"\tmov \tr1, {other.register}\n")
        file.write("\tbl  \t__aeabi_idiv\n")
        # Place result in new register.
        file.write(f"\tmov \t{scratchRegister}, r0\n")
        # Restore original values.
        file.write("\tpop \t {r0, r1}\n")
        if(other.value == 0):           # Since we're compiling, doesn't matter.
            return Number(self.value / 1, self.lineNumber, scratchRegister)
        return Number(self.value / other.value, self.lineNumber, scratchRegister)

    # Equality :: Number -> Number
    def Equality(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.registers.pop(0)
        tempRegister = context.registers[0]                        # Used since we don't want the original register to change.
        file.write(f"\tsub \t{tempRegister}, {other.register}, {self.register}\n")
        file.write(f"\tneg \t{scratchRegister}, {tempRegister}\n")
        file.write(f"\tadc \t{scratchRegister}, {scratchRegister}, {tempRegister}\n")
        return Number(int(self.value == other.value), self.lineNumber, scratchRegister) # Scratchregister contains result.

    # NonEquality :: Number -> Number    
    def NonEquality(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        file.write(f"\tsub \t{scratchRegister}, {other.register}, {self.register}\n")
        file.write(f"\tsub \t{tempRegister}, {scratchRegister}, #1\n")
        file.write(f"\tsbc \t{scratchRegister}, {scratchRegister}, {tempRegister}\n")
        return Number(int(self.value != other.value), self.lineNumber, scratchRegister)

    # Less :: Number -> Number
    def Less(self, other : 'Number', context: Context, file) -> 'Number':
        """" Scratch register contains 1 afterwards when smaller. """
        scratchRegister = context.registers.pop(0)
        segment = context.segments.pop(0)
        file.write(f"\tmov \t{scratchRegister}, #1\n")
        file.write(f"\tcmp \t{self.register}, {other.register}\n")
        file.write(f"\tblt \t{segment}\n")
        file.write(f"\tmovs\t{scratchRegister}, #0\n")
        file.write(f"{segment}:\n")
        return Number(int(self.value < other.value), self.lineNumber, scratchRegister)

    # Greater :: Number -> Number
    def Greater(self, other : 'Number', context: Context, file) -> 'Number':
        """" Scratch register contains 1 afterwards when greater. """
        scratchRegister = context.registers.pop(0)
        segment = context.segments.pop(0)
        file.write(f"\tmov \t{scratchRegister}, #1\n")
        file.write(f"\tcmp \t{self.register}, {other.register}\n")
        file.write(f"\tbgt \t{segment}\n")
        file.write(f"\tmovs\t{scratchRegister}, #0\n")
        file.write(f"{segment}:\n")
        return Number(int(self.value > other.value), self.lineNumber, scratchRegister)

    # LessEqual :: Number -> Number
    def LessEqual(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        file.write(f"\tlsr \t{scratchRegister}, {self.register}, #31\n")
        file.write(f"\tasr \t{tempRegister}, {other.register}, #31\n")
        file.write(f"\tcmp \t{other.register}, {self.register}\n")
        file.write(f"\tadc \t{scratchRegister}, {scratchRegister}, {tempRegister}\n")
        return Number(int(self.value <= other.value), self.lineNumber, scratchRegister)

    # GreaterEqual :: Number -> Number
    def GreaterEqual(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        file.write(f"\tasr \t{scratchRegister}, {self.register}, #31\n")
        file.write(f"\tlsr \t{tempRegister}, {other.register}, #31\n")
        file.write(f"\tcmp \t{self.register}, {other.register}\n")
        file.write(f"\tadc \t{scratchRegister}, {scratchRegister}, {tempRegister}\n")
        return Number(int(self.value >= other.value), self.lineNumber, scratchRegister)

    # And :: Number -> Number
    def And(self, other : 'Number', context: Context, file) -> 'Number':
        resultRegister = context.registers.pop(0)
        firstRegister = context.registers[0]
        otherRegister = context.registers[1]
        file.write(f"\tasr \t{firstRegister}, {self.register}, #31\n")
        file.write(f"\tsub \t{resultRegister}, {firstRegister}, {self.register}\n")
        file.write(f"\tasr \t{firstRegister}, {other.register}, #31\n")
        file.write(f"\tsub \t{otherRegister}, {firstRegister}, {other.register}\n")
        file.write(f"\tand \t{resultRegister}, {resultRegister}, {otherRegister}\n")
        file.write(f"\tlsr \t{resultRegister}, {resultRegister}, #31\n")
        return Number(int(self.value and other.value), self.lineNumber, resultRegister)

    # Or :: Number -> Number
    def Or(self, other : 'Number', context: Context, file) -> 'Number':
        print(context.registers)
        resultRegister = context.registers.pop(0)
        firstRegister = context.registers[0]
        otherRegister = context.registers[1]
        file.write(f"\tasr \t{firstRegister}, {self.register}, #31\n")
        file.write(f"\tsub \t{resultRegister}, {firstRegister}, {self.register}\n")
        file.write(f"\tasr \t{firstRegister}, {other.register}, #31\n")
        file.write(f"\tsub \t{otherRegister}, {firstRegister}, {other.register}\n")
        file.write(f"\torr \t{resultRegister}, {resultRegister}, {otherRegister}\n")
        file.write(f"\tlsr \t{resultRegister}, {resultRegister}, #31\n")
        return Number(int(self.value or other.value), self.lineNumber, resultRegister)

    # __bool__ -> Boolean
    def __bool__(self) -> bool:
        return self.value != 0

    # __repr__ -> String
    def __repr__(self) -> str:
        return str(self.value)
