# SPDX-FileCopyrightText: © 2021 Jochem van Kranenburg <jochem.vankranenburg@outlook.com>
# PDX-License-Identifier: AGPL-3.0 License

from typing import Union, List
from interpret.context import Context

class Number():
    """ Compile numbers
    This class contains the ability to compile numbers and their operators.
    Hence, this class is practically the heart of the compiler.

    Most methods are very trivial and easy to understand. There are, however,
    a couple of comparison operators that have turned out quite large.

    This is because of the nature of SRPL. Furthermore, the  chosen implementation 
    doesn't require distinguishing wether the comparison is for a variable 
    assignment or an if-statement; way less code and easier to understand.
    """

    # __init__ :: Integer | Float -> Integer -> Nothing
    def __init__(self, value : Union[int, float], lineNumber : int, register : str):
        self.value = value
        self.lineNumber = lineNumber
        self.register = register

    # Add :: Number -> Number
    def Add(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        file.append(f'\tadd \t{self.register}, {other.register} \
        \t\t\t@ Register {self.register} contains result from addition of registers {self.register} and {other.register}.\n')
        return Number(self.value + other.value, self.lineNumber, self.register)

    # Substract :: Number -> Number
    def Substract(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        file.append(f'\tsub \t{self.register}, {other.register} \
        \t\t\t@ Register {self.register} contains result from substraction of registers {self.register} and {other.register}.\n')
        return Number(self.value - other.value, self.lineNumber, self.register)

    # Multiply :: Number -> Number
    def Multiply(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        file.append(f'\tmul \t{self.register}, {self.register}, {other.register} \
        \t\t@ Register {self.register} contains result from multiplication of registers {self.register} and {other.register}.\n')
        return Number(self.value * other.value, self.lineNumber, self.register)

    # Divide :: Number -> Number
    def Divide(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        """ Divide numbers
        The division of numbers might seem trivial, but for a Cortex M0 it isn't. Division
        isn't something that's possible with one instruction. Luckily GNU Arm Embedded Toolchain has
        a neat subroutine for that. This requires that the numbers to divide are placed in r0 and 1.

        Please note that the popped register is added to the set of used registers at index 5 of the file.
        All functions that use registers should add the highest used register to that set so the compiler
        can determine what registers should be restored after function completion. This is used everywhere.

        Parameters:
            other (Number): The number to use for dividing this number (self).
            context (Context): The context to use for 'allocating' registers.
            file (List[str]): The 'file' to write the assembly code into.

        Returns:
            Number: The result of the operation; neccesary to allow for further compilation.
        """
        resultRegister = context.registers.pop(0)
        file[5].add(resultRegister)
        file.append("\tpush\t{r0, r1}\t\t\t\t@ Push original values to stack.\n")
        file.append(f"\tmov \tr0, {self.register}\t\t\t\t\t@ Move registers to divide to r0 and r1.\n")
        file.append(f"\tmov \tr1, {other.register}\n")
        file.append("\tbl  \t__aeabi_idiv\n")
        file.append(f"\tmov \t{resultRegister}, r0\t\t\t\t\t@ Store result of division in {resultRegister}.\n")
        file.append("\tpop \t{r0, r1}\t\t\t\t@ Restore original values of r0 and r1.\n")
        if(other.value == 0):           # Since we're compiling, divide by zero doesn't matter; GCC will already complain about that.
            return Number(self.value / 1, self.lineNumber, resultRegister)
        return Number(self.value / other.value, self.lineNumber, resultRegister)

    # Equality :: Number -> Number
    def Equality(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        """ Equal numbers
        No documentation needed (so trivial), but one quick note; there's a temporarily required
        register that can be used again later on. That's why it isn't popped from the context, 
        but just accessed. This is used more often.
        """
        resultRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        file[5].add(tempRegister)
        file.append(f"\tsub \t{tempRegister}, {other.register}, {self.register}\n")
        file.append(f"\tneg \t{resultRegister}, {tempRegister}\n")
        file.append(f"\tadc \t{resultRegister}, {resultRegister}, {tempRegister}\t\t\
        @ Register {resultRegister} contains wether {self.register} and {other.register} are equal.\n")
        return Number(int(self.value == other.value), self.lineNumber, resultRegister)

    # NonEquality :: Number -> Number    
    def NonEquality(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        resultRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        file[5].add(tempRegister)
        file.append(f"\tsub \t{resultRegister}, {other.register}, {self.register}\n")
        file.append(f"\tsub \t{tempRegister}, {resultRegister}, #1\n")
        file.append(f"\tsbc \t{resultRegister}, {resultRegister}, {tempRegister}\t\t\
        @ Register {resultRegister} contains wether {self.register} and {other.register} are not equal.\n")
        return Number(int(self.value != other.value), self.lineNumber, resultRegister)

    # Less :: Number -> Number
    def Less(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        """ Is number less
        Again a trivial function, but the first one with this structure. The label and branching to
        that label is used to only place a zero in the result(scratch) register when it isn't less
        than the other register. This structure is also used with the greater than operator.
        """
        resultRegister = context.registers.pop(0)
        file[5].add(resultRegister)
        label = context.labels.pop(0)
        file.append(f"\tmov \t{resultRegister}, #1\n")
        file.append(f"\tcmp \t{self.register}, {other.register}\n")
        file.append(f"\tblt \t{label}\n")                               # Branch past moving zero into result.
        file.append(f"\tmovs\t{resultRegister}, #0\n")
        file.append(f"{label}:\t\t\t\t\t\t\t\t@ Register {resultRegister} contains wether {self.register} is less than {other.register}.\n")
        return Number(int(self.value < other.value), self.lineNumber, resultRegister)

    # Greater :: Number -> Number
    def Greater(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        """" Scratch register contains 1 afterwards when greater. """
        resultRegister = context.registers.pop(0)
        file[5].add(resultRegister)
        label = context.labels.pop(0)
        file.append(f"\tmov \t{resultRegister}, #1\n")
        file.append(f"\tcmp \t{self.register}, {other.register}\n")
        file.append(f"\tbgt \t{label}\n")
        file.append(f"\tmovs\t{resultRegister}, #0\n")
        file.append(f"{label}:\t\t\t\t\t\t\t\t@ Register {resultRegister} contains wether {self.register} is greater than {other.register}.\n")
        return Number(int(self.value > other.value), self.lineNumber, resultRegister)

    # LessEqual :: Number -> Number
    def LessEqual(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        resultRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        file[5].add(tempRegister)
        file.append(f"\tlsr \t{resultRegister}, {self.register}, #31\n")
        file.append(f"\tasr \t{tempRegister}, {other.register}, #31\n")
        file.append(f"\tcmp \t{other.register}, {self.register}\n")
        file.append(f"\tadc \t{resultRegister}, {resultRegister}, {tempRegister}\t\t\
        @ Register {resultRegister} contains wether {self.register} is less than or equal to {other.register}.\n")
        return Number(int(self.value <= other.value), self.lineNumber, resultRegister)

    # GreaterEqual :: Number -> Number
    def GreaterEqual(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        resultRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        file[5].add(tempRegister)
        file.append(f"\tasr \t{resultRegister}, {self.register}, #31\n")
        file.append(f"\tlsr \t{tempRegister}, {other.register}, #31\n")
        file.append(f"\tcmp \t{self.register}, {other.register}\n")
        file.append(f"\tadc \t{resultRegister}, {resultRegister}, {tempRegister}\t\t\
        @ Register {resultRegister} contains wether {self.register} is greater than or equal to {other.register}.\n")
        return Number(int(self.value >= other.value), self.lineNumber, resultRegister)

    # And :: Number -> Number
    def And(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        resultRegister = context.registers.pop(0)
        firstRegister = context.registers[0]
        otherRegister = context.registers[1]
        file[5].add(otherRegister)
        file.append(f"\tasr \t{firstRegister}, {self.register}, #31\n")
        file.append(f"\tsub \t{resultRegister}, {firstRegister}, {self.register}\n")
        file.append(f"\tasr \t{firstRegister}, {other.register}, #31\n")
        file.append(f"\tsub \t{otherRegister}, {firstRegister}, {other.register}\n")
        file.append(f"\tand \t{resultRegister}, {resultRegister}, {otherRegister}\n")
        file.append(f"\tlsr \t{resultRegister}, {resultRegister}, #31\t\t\
        @ Register {resultRegister} contains wether {self.register} and {other.register} are both larger than 0.\n")
        return Number(int(self.value and other.value), self.lineNumber, resultRegister)

    # Or :: Number -> Number
    def Or(self, other : 'Number', context: Context, file: List[str]) -> 'Number':
        resultRegister = context.registers.pop(0)
        firstRegister = context.registers[0]
        otherRegister = context.registers[1]
        file[5].add(otherRegister)
        file.append(f"\tasr \t{firstRegister}, {self.register}, #31\n")
        file.append(f"\tsub \t{resultRegister}, {firstRegister}, {self.register}\n")
        file.append(f"\tasr \t{firstRegister}, {other.register}, #31\n")
        file.append(f"\tsub \t{otherRegister}, {firstRegister}, {other.register}\n")
        file.append(f"\torr \t{resultRegister}, {resultRegister}, {otherRegister}\n")
        file.append(f"\tlsr \t{resultRegister}, {resultRegister}, #31\t\t\
        @ Register {resultRegister} contains wether {self.register} or {other.register} is larger than 0.\n")
        return Number(int(self.value or other.value), self.lineNumber, resultRegister)

    # __bool__ -> Boolean
    def __bool__(self) -> bool:
        return self.value != 0

    # __repr__ -> String
    def __repr__(self) -> str:
        return str(self.value)
