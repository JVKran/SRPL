from typing import List, Optional
from operator import is_not, add
from functools import partial, reduce
from itertools import chain
from copy import copy

from parse.nodes import *
from compile.context import Context
from compile.number import Number
from compile.function import Function
from lex.token import *

class Compiler():

    # __init__ :: String -> String -> FunctionNode
    def __init__(self, sourceFile: str, targetFile: str, function: FunctionNode):
        """ Initialize compiler
        Intialize the compiler by providing some feedback to the user and opening the
        possibly already existing file. Previous contents are overwritten.

        Please note that registers 4 to 8 are always pushed, regardless of them being
        used or not. This has been done to minimize complexity. Furthermore, these few
        stack pushes and pops aren't that cpu intensive.

        Parameters:
            sourceFile (str): The name of the SRPL sourcefile to compile.
            targetFile (str): The name of the assembly targetfile to write to.
        """
        self.context = Context(f"<{sourceFile}>")
        self.function = function
        self.targetFile = targetFile
        print("Compiling \'" + sourceFile + "\' to \'" + targetFile + "\'.")


        self.file: List[str] = []
        self.file.append("\t.cpu cortex-m0\n")
        self.file.append("\t.text\n")
        self.file.append("\t.align 2\n")
        self.file.append(f"\t.global {function.name}\n\n")
        self.file.append(f'{function.name}:\n')
        self.file.append(set())

    def __del__(self):
        """ Destruct compiler
        But before the compiler is not needed anymore, the result has to be written to the
        targetfile. Beforehand, the used registers are determined. This is done by checking
        the fifth index of the 'file'; this contains a set with the highest used registers.

        After this has been determined, the compiled assembly code is written to the targetfile.
        """
        registers = ["r4", "r5", "r6", "r7", "r8"]
        try:
            highestRegisterIndex: int = registers.index(max(self.file[5]))
            usedRegisters: str = registers[0:highestRegisterIndex + 1]
        except ValueError:
            usedRegisters = []
        usedRegisters: str = ', '.join(usedRegisters)           # Create comma separated string with registers.
        if len(usedRegisters) > 0:
            registersToPop = f"\tpop \t{{ {usedRegisters}, pc }}"
            registersToPush = f"\tpush \t{{ {usedRegisters}, lr }}\n"
        else:
            registersToPop = f"\tpop \t{{ pc }}"
            registersToPush = f"\tpush \t{{ lr }}\n"
        self.file.append(registersToPop)
        self.file[5] = registersToPush

        file = open(self.targetFile, "w")
        for line in self.file:                                  # TODO: Replace with map
            file.write(line)
        file.close()
    
    def compile(self, node: Node, context: Optional[Context] = None) -> Optional[Union[Number, List[Number], Function]]:
        """ Compile node
        Compile node by visiting all nodes in the Abstract Syntax Tree. For this to be possible,
        all nodes have to be 'created'. This means that all calculations are still made, functions
        are still called and while loops are still executed. Note that this, however, only happens 
        once to determine what numbers are created and thus what registers have to be used in what
        way.

        This can also be concluded by the fact that the structure of the code for the compiler 
        largeley resembles that of the interpreter; they're practically the same.

        Parameters:
            node (Node): The node to compile(/visit).
            context (Context): The context to use for allocating registers and labels.
        """
        if not context:             # If no context has been given; use new context.
            context = self.context

        # compileOperatorNode :: OperatorNode -> Context -> Number
        def compileOperatorNode(node: OperatorNode, context: Context) -> Number:
            """ Compile operator
            Compilation of the operator and/or the result thereof is delegated to the Number.
            For that to be possible, the method to call is determined before it's executed.

            Parameters:
                node (OperatorNode): The operator node to compile.
                context (Context): The context to use for allocating registers and labels.

            Returns:
                Number: The result of execution of the operator.
            """
            left = self.compile(node.left_node, context)
            right = self.compile(node.right_node, context)
            methodName = f'{type(node.operator).__name__}'.replace("Token", '')         # AddToken becomes Add, MultiplyToken becomes Multiply, etc.
            method = getattr(left, methodName)
            res = method(right, context, self.file)
            return res

        # compileNumbernode :: NumberNode -> Context -> Number
        def compileNumberNode(node: NumberNode, context: Context) -> Number:
            """ Compile number
            Compilation of numbernodes consists of two responsibilities; creating the number to
            allow traversing of the AST and allocating a register with the desired value.

            Parameters:
                node (NumberNode): The number node to compile.
                context (Context): The context to use for allocating registers and labels.

            Returns:
                Number: The resulting number object.
            """
            availableRegister = context.registers.pop(0)
            number = Number(node.token.stringToParse, node.token.lineNumber, availableRegister)
            self.file.append(f"\tmovs\t{availableRegister}, #{number.value}\n")
            return number

        # compileVariableNode :: VariableNode -> Context -> Number
        def compileVariableNode(node: VariableNode, context: Context) -> Number:
            """ Compile variable
            Compilation of variablenodes consists of one of two possible tasks; getting the value
            of the requested symbol to allow for interpretation and thus full translation of the 
            function or the compilation of the expression to be evaluated for determining the value
            of the variable node.

            Parameters:
                node (VariableNode): The variable node to compile.
                context (Context): The context to use for allocating registers and labels and requesting
                                    symbol values.

            Returns:
                Number: A number with the desired and/or resulting value.
            """
            if node.value == None:
                variableName = node.var_name.stringToParse
                value = context.getSymbol(variableName)
            else:
                variableName = node.var_name
                value = self.compile(node.value, context)
                context.symbols[variableName] = value
            return value

        # compileIfNode :: IfNode -> Context -> Number | Nothing
        def compileIfNode(node: IfNode, context: Context) -> Optional[Number]:
            """ Compile if-statement
            The if-statement is compiled by first compiling the condition and then comparing the result
            with '1'. When this is equal, the condition is true and the compiled expression is to be executed
            while when this isn't equal, the program should branch to the label after the expression to execute
            when the condition is met. Same goes for the else-expression.

            Parameters:
                node (IfNode): The if node to compile.
                context (Context): The context to use for allocating registers and labels.

            Returns:
                Number: The optional result of the if and/or else expression.
            """
            conditionIsMet: Number = self.compile(node.condition, context)
            availableRegisters = copy(context.registers)                        # Save registers since the condition is either true, or false.
            self.file.append(f"\tcmp \t{conditionIsMet.register}, #1\n")         # Hence, the registers are used in one single case; not both.
            afterIf = context.labels.pop(0)
            afterElse = context.labels.pop(0)
            self.file.append(f"\tbne \t{afterIf}\n")                             # If condition isn't met; go to label after expression to be executed when condition is true.
            resReg = context.registers[0]
            res = self.compile(node.expression, context)
            self.file.append(f"\tb   \t{afterElse} \n")                          # Don't also execute else-expression; so branch to label after else expression.
            self.file.append(f"{afterIf}:\n")
            context.registers = availableRegisters
            if node.elseExpression:
                self.compile(node.elseExpression, context)
                if(type(node.elseExpression) == CallNode):
                    self.file.append(f"\tmovs\t{resReg}, r0\n")                  # Inherent to the way SRPL deals with variables and return values.
            self.file.append(f"{afterElse}:\n")
            return res

        # compileWhileNode :: WhileNode -> Context -> Nothing
        def compileWhileNode(node: WhileNode, context: Context) -> None:
            """ Compile while-loop
            The while-loop can't be easier than this... Execute the codeSequence and
            branch back to start of the codesequence as long as condition equals to 1.
            Otherwise; continue with next assembly code.

            Parameters:
                node (WhileNode): The while node to compile.
                context (Context): The context to use for allocating registers and labels.
            """
            self.file.append("loop:\n")
            conditionIsMet: Number = self.compile(node.condition, context)
            self.compile(node.codeSequence, context)
            self.file.append(f"\tcmp \t{conditionIsMet.register}, #1\n")
            self.file.append(f"\tbeq \tloop\n")                                  # If condition is met; go back to loop label.

        # compileFunctionNode :: FunctionNode -> Context -> Function
        def compileFunctionNode(node: FunctionNode, context: Context) -> Function:
            """ Compile function
            The function node is (again) very easy to compile; a lot is delegated to the other 
            functions of course. Just add the function to the symbol table, allocate registers
            for the parameters and 'execute' the function so the nodes in the functionbody can
            also be compiled.

            Parameters:
                node (FunctionNode): The function node to compile.
                context (Context): The context to use for allocating registers and labels.

            Returns:
                Function: The compiled function.
            """
            functionValue = Function(node.name, node.codeSequence, node.arguments, context)
            context.symbols[node.name] = functionValue
            arguments = [Number(0, 0, context.registers.pop(0)) for _ in range(len(node.arguments))]           # TODO: Make functional.
            codeSequence, context = functionValue.execute(arguments, context)
            return self.compile(codeSequence, context)

        # compileCallNode :: CallNode -> Context -> Nothing
        def compileCallNode(node: CallNode, context: Context) -> None:
            """ Compile function call
            In contrary of the compileFunctionNode function, we don't have to allocate registers;
            we have to make sure the evaluated values are placed in the registers. After this has
            been done we're able to branch right into the function!

            Parameters:
                node (CallNode): The call node to compile.
                context (Context): The context to use for allocating registers and labels.
            """
            arguments: List[Number] = []
            if node.argumentNodes != None:
                arguments = list(chain(*map(lambda node: [*arguments, self.compile(node, context)], node.argumentNodes)))
            self.file.append(f"\tbl  \t{node.nodeToCall.var_name.stringToParse}\n")

        # compileListNode :: ListNode -> Context -> Number | [Number]
        def compileListNode(node: ListNode, context: Context) -> Union[Number, List[Number]]:
            """ Compile list node.
            This method might require some more explanation. This method determines
            the result of all nodes in the 'list'. These lists can occur since functions,
            but also files, are allowed to return 'flush' multiple values. So, for example,
            when a function returns once, there will only be one element in the returned list.
            But when a function doesn't return at all, the results of all nodes will be in 
            the list. Same goes for functions or files returning multiple times; a list
            will be returned.

            Functions exactly the same as with the interpreter; only required for compatibilty
            with other code since the parser still returns ListNodes.

            Parameters:
                node (ListNode): The node with node(s) to be compiled.
                context (Context): The context to use for allocating registers and labels.

            Returns:
                Number: A (possibly list of) Number(s) with the result of the expression.
            """
            returnNodes = map(lambda element: ReturnNode == type(element), node.elementNodes)
            returnPresent: Number = reduce(add, returnNodes, 0)                         # Are there any nodes that really flush something?
            
            def compileElement(elementNode):
                if not returnPresent:
                    return self.compile(elementNode, context)
                elif type(elementNode) == ReturnNode:
                    return self.compile(elementNode, context)
                self.compile(elementNode, context)

            elements: List[Number] = []
            elements = list(chain(*map(lambda node: [*elements, compileElement(node)], node.elementNodes)))
            elements = list(filter(partial(is_not, None), elements))            # Filter all None values. Note that None is equal to 0, so is_not is used.
            
            if len(elements) == 1:
                return elements[0]
            return elements

        # compileReturnNode :: ReturnNode -> Context -> Number | Nothing
        def compileReturnNode(node: ReturnNode, context: Context) -> Optional[Number]:
            """ Compile return
            A return statement translates to a label to branch to and the placement of
            the result (the variable to be returned) in r0. Nothing more, nothing less.

            Parameters:
                node (ReturnNode): The return node to be compiled.
                context (Context): The context to use for allocating registers and labels.

            Returns:
                Number: The value to return.
            """
            if node.nodeToReturn:
                res = self.compile(node.nodeToReturn, context)
                self.file.append("end:\n")
                self.file.append(f"\tmovs\tr0, {res.register}\n")
                return res

        functionName: str = f'compile{type(node).__name__}'                         # Determine name of function to call.
        function = locals()[functionName]                                           # Get function with corresponding name.
        return function(node, self.context)
