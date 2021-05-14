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
        file.append(f'\tadd \t{self.register}, {other.register}\n')
        return Number(self.value + other.value, self.lineNumber, self.register)

    # Substract :: Number -> Number
    def Substract(self, other : 'Number', context: Context, file) -> 'Number':
        file.append(f'\tsub \t{self.register}, {other.register}\n')
        return Number(self.value - other.value, self.lineNumber, self.register)

    # Multiply :: Number -> Number
    def Multiply(self, other : 'Number', context: Context, file) -> 'Number':
        file.append(f'\tmul \t{self.register}, {self.register}, {other.register}\n')            # Multiply self with other and store in self.
        return Number(self.value * other.value, self.lineNumber, self.register)

    # Divide :: Number -> Number
    def Divide(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.registers.pop(0)
        file[5].add(scratchRegister)
        file.append("\tpush\t{r0, r1}\t\t@Push original values to stack.\n")
        file.append(f"\tmov \tr0, {self.register}\t\t@Move registers to devide to r0 and r1.\n")
        file.append(f"\tmov \tr1, {other.register}\n")
        file.append("\tbl  \t__aeabi_idiv\n")
        # Place result in new register.
        file.append(f"\tmov \t{scratchRegister}, r0\t\t@Store result in new register.\n")
        # Restore original values.
        file.append("\tpop \t{r0, r1}\t\t@Restore original values of r0 and r1.\n")
        if(other.value == 0):           # Since we're compiling, doesn't matter.
            return Number(self.value / 1, self.lineNumber, scratchRegister)
        return Number(self.value / other.value, self.lineNumber, scratchRegister)

    # Equality :: Number -> Number
    def Equality(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.registers.pop(0)
        tempRegister = context.registers[0]                        # Used since we don't want the original register to change.
        file[5].add(tempRegister)
        file.append(f"\tsub \t{tempRegister}, {other.register}, {self.register}\n")
        file.append(f"\tneg \t{scratchRegister}, {tempRegister}\n")
        file.append(f"\tadc \t{scratchRegister}, {scratchRegister}, {tempRegister}\t\t@Register {scratchRegister} contains wether {self.register} and {other.register} are equal.\n")
        return Number(int(self.value == other.value), self.lineNumber, scratchRegister) # Scratchregister contains result.

    # NonEquality :: Number -> Number    
    def NonEquality(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        file[5].add(tempRegister)
        file.append(f"\tsub \t{scratchRegister}, {other.register}, {self.register}\n")
        file.append(f"\tsub \t{tempRegister}, {scratchRegister}, #1\n")
        file.append(f"\tsbc \t{scratchRegister}, {scratchRegister}, {tempRegister}\t\t@Register {scratchRegister} contains wether {self.register} and {other.register} are not equal.\n")
        return Number(int(self.value != other.value), self.lineNumber, scratchRegister)

    # Less :: Number -> Number
    def Less(self, other : 'Number', context: Context, file) -> 'Number':
        """" Scratch register contains 1 afterwards when smaller. """
        scratchRegister = context.registers.pop(0)
        file[5].add(scratchRegister)
        label = context.labels.pop(0)
        file.append(f"\tmov \t{scratchRegister}, #1\n")
        file.append(f"\tcmp \t{self.register}, {other.register}\n")
        file.append(f"\tblt \t{label}\n")
        file.append(f"\tmovs\t{scratchRegister}, #0\n")
        file.append(f"{label}:\t\t\t\t\t@Register {scratchRegister} contains wether {self.register} is less than {other.register}.\n")
        return Number(int(self.value < other.value), self.lineNumber, scratchRegister)

    # Greater :: Number -> Number
    def Greater(self, other : 'Number', context: Context, file) -> 'Number':
        """" Scratch register contains 1 afterwards when greater. """
        scratchRegister = context.registers.pop(0)
        file[5].add(scratchRegister)
        label = context.labels.pop(0)
        file.append(f"\tmov \t{scratchRegister}, #1\n")
        file.append(f"\tcmp \t{self.register}, {other.register}\n")
        file.append(f"\tbgt \t{label}\n")
        file.append(f"\tmovs\t{scratchRegister}, #0\n")
        file.append(f"{label}:\t\t\t\t\t@Register {scratchRegister} contains wether {self.register} is greater than {other.register}.\n")
        return Number(int(self.value > other.value), self.lineNumber, scratchRegister)

    # LessEqual :: Number -> Number
    def LessEqual(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        file[5].add(tempRegister)
        file.append(f"\tlsr \t{scratchRegister}, {self.register}, #31\n")
        file.append(f"\tasr \t{tempRegister}, {other.register}, #31\n")
        file.append(f"\tcmp \t{other.register}, {self.register}\n")
        file.append(f"\tadc \t{scratchRegister}, {scratchRegister}, {tempRegister}\t\t@Register {scratchRegister} contains wether {self.register} is less than or equal to {other.register}.\n")
        return Number(int(self.value <= other.value), self.lineNumber, scratchRegister)

    # GreaterEqual :: Number -> Number
    def GreaterEqual(self, other : 'Number', context: Context, file) -> 'Number':
        scratchRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        file[5].add(tempRegister)
        file.append(f"\tasr \t{scratchRegister}, {self.register}, #31\n")
        file.append(f"\tlsr \t{tempRegister}, {other.register}, #31\n")
        file.append(f"\tcmp \t{self.register}, {other.register}\n")
        file.append(f"\tadc \t{scratchRegister}, {scratchRegister}, {tempRegister}\t\t@Register {scratchRegister} contains wether {self.register} is greater than or equal to {other.register}.\n")
        return Number(int(self.value >= other.value), self.lineNumber, scratchRegister)

    # And :: Number -> Number
    def And(self, other : 'Number', context: Context, file) -> 'Number':
        resultRegister = context.registers.pop(0)
        firstRegister = context.registers[0]
        otherRegister = context.registers[1]
        file[5].add(otherRegister)
        file.append(f"\tasr \t{firstRegister}, {self.register}, #31\n")
        file.append(f"\tsub \t{resultRegister}, {firstRegister}, {self.register}\n")
        file.append(f"\tasr \t{firstRegister}, {other.register}, #31\n")
        file.append(f"\tsub \t{otherRegister}, {firstRegister}, {other.register}\n")
        file.append(f"\tand \t{resultRegister}, {resultRegister}, {otherRegister}\n")
        file.append(f"\tlsr \t{resultRegister}, {resultRegister}, #31\t\t@Register {resultRegister} contains wether {self.register} and {other.register} are both larger than 0.\n")
        return Number(int(self.value and other.value), self.lineNumber, resultRegister)

    # Or :: Number -> Number
    def Or(self, other : 'Number', context: Context, file) -> 'Number':
        print(context.registers)
        resultRegister = context.registers.pop(0)
        firstRegister = context.registers[0]
        otherRegister = context.registers[1]
        file[5].add(otherRegister)
        file.append(f"\tasr \t{firstRegister}, {self.register}, #31\n")
        file.append(f"\tsub \t{resultRegister}, {firstRegister}, {self.register}\n")
        file.append(f"\tasr \t{firstRegister}, {other.register}, #31\n")
        file.append(f"\tsub \t{otherRegister}, {firstRegister}, {other.register}\n")
        file.append(f"\torr \t{resultRegister}, {resultRegister}, {otherRegister}\n")
        file.append(f"\tlsr \t{resultRegister}, {resultRegister}, #31\t\t@Register {resultRegister} contains wether {self.register} or {other.register} is larger than 0.\n")
        return Number(int(self.value or other.value), self.lineNumber, resultRegister)

    # __bool__ -> Boolean
    def __bool__(self) -> bool:
        return self.value != 0

    # __repr__ -> String
    def __repr__(self) -> str:
        return str(self.value)
