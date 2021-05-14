from typing import TypeVar, Union, Optional, List
from operator import is_not, add
from functools import partial, reduce
from itertools import chain

from parse.nodes import *
from interpret.context import Context
from interpret.number import Number
from interpret.function import Function

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

# visit :: Node -> Context -> Number | [Number]
def visit(node : Node, context : Context) -> Union[Number, List[Number]]:
    """ Visit node
    This function visits a node and delegates the 'real' interpretation to their
    corresponding inner-function. The entire Abstract Syntax Tree is interpreted
    this way.

    Parameters:
        node (Node): Intially the root-node, but after first interpretation also other nodes.
        context (Context): The context to use for interpretation.
    """

    # visitOperatorNode :: OperatorNode -> Context -> Number
    def visitOperatorNode(node : OperatorNode, context : Context) -> Number:
        """ Interpret operator
        Interpretation of the operator and/or the result thereof is delegated to the Number.
        For that to be possible, the method to call is determined before it's executed.

        Parameters:
            node (OperatorNode): The operator node to interpret.
            context (Context): The context to use for interpretation.

        Returns:
            Number: The result of execution of the operator.
        """
        left = visit(node.left_node, context)
        right = visit(node.right_node, context)
        methodName = f'{type(node.operator).__name__}'.replace("Token", '')         # AddToken becomes Add, MultiplyToken becomes Multiply, etc.
        method = getattr(left, methodName)
        return method(right)

    # visitNumbernode :: NumberNode -> Context -> Number
    def visitNumberNode(node : NumberNode, context : Context) -> Number:
        """ Interpret number
        Interpretation of numbers is as trivial as can be; entirely delegated to Number.

        Parameters:
            node (NumberNode): The number node to compile.
            context (Context): The context to use for allocating registers and labels.

        Returns:
            Number: The resulting number object.
        """
        return Number(node.token.stringToParse, node.token.lineNumber)

    # visitVariableNode :: VariableNode -> Context -> Number
    def visitVariableNode(node : VariableNode, context : Context) -> Number:
        """ Interpret variable 
        Retrieves the value of a variable from the symboltable or stores the value of said
        variable in the symboltable.

        Parameters:
            node (VariableNode): The variable node to interpret.
            context (Context): The context to use for retrieving or storing variable value.

        Returns:
            Number: A number with the desired and/or resulting value.
        """
        if node.value == None:
            variableName = node.var_name.stringToParse
            value = context.getSymbol(variableName)
        else:
            variableName = node.var_name
            value = visit(node.value, context)
            context.symbols[variableName] = value
        return value

    def visitIfNode(node : IfNode, context : Context) -> Optional[Number]:
        """ Interpret if-statement
        Execute expression of if statement when condition is met or exepression 
        of else statement when provided. 
        
        Parameters:
            node (IfNode): The if node to interpret.
            context (Context): The context to use for interpretation of condition and expression(s).

        Returns:
            Number: The optional result of the if and/or else expression.
        """
        conditionIsMet: Number = visit(node.condition, context)
        if conditionIsMet:
            return visit(node.expression, context)
        elif node.elseExpression:
            return visit(node.elseExpression, context)
        return None

    # visitWhileNode :: WhileNode -> Context -> Nothing
    def visitWhileNode(node : WhileNode, context : Context) -> None:
        """ Interpret while-loop
        Execute the while-body for as long as the condition is met.

        Parameters:
            node (WhileNode): The while node to interpret.
            context (Context): The context to use for interpreting condition and body.
        """
        conditionIsMet: Number = visit(node.condition, context)
        if conditionIsMet:
            visit(node.codeSequence, context)           # Execute while-body once.
            return visitWhileNode(node, context)        # Then check for meeting condition.
        return

    # visitFunctionNode :: FunctionNode -> Context -> Function
    def visitFunctionNode(node : FunctionNode, context : Context) -> Function:
        """ Interpret function
        Create function from function definition and add the resulting definition
        to the symboltable.

        Parameters:
            node (FunctionNode): The function node to interpret.
            context (Context): The context to use for interpretation of function and to 
                                add the definition to.

        Returns:
            Function: The function definition.
        """
        functionValue = Function(node.name, node.codeSequence, node.arguments, context)
        context.symbols[node.name] = functionValue
        return functionValue

    # visitCallNode :: CallNode -> Context -> Number | Nothing
    def visitCallNode(node : CallNode, context : Context) -> Optional[Number]:
        """ Interpret function call
        Interpret function call after argument values have been determined.

        Parameters:
            node (CallNode): The call node to interpret.
            context (Context): The context to use for determining argumentvalues and execution of the function.

        Returns:
            Number: Function result.
        """
        arguments: List[Number] = []
        valueToCall = visit(node.nodeToCall, context)

        # The notation [*arguments, visit(node, context)] is a sneaky way of appending values to a list that returns the list.
        # The append method works fine, but only appends to the object; it doesn't return the list with appended values. Used multiple times.
        if node.argumentNodes != None:
            arguments = list(chain(*map(lambda node: [*arguments, visit(node, context)], node.argumentNodes)))

        return valueToCall.execute(arguments, context)

    # visitListNode :: ListNode -> Context -> Number | [Number]
    def visitListNode(node : ListNode, context : Context) -> Union[Number, List[Number]]:
        """ Interpret list node
        This method might require some more explanation. This method determines
        the result of all nodes in the 'list'. These lists can occur since functions,
        but also files, are allowed to return 'flush' multiple values. So, for example,
        when a function returns once, there will only be one element in the returned list.
        But when a function doesn't return at all, the results of all nodes will be in 
        the list. Same goes for functions or files returning multiple times; a list
        will be returned.

        Parameters:
            node (ListNode): The list node to interpret.
            context (Context): The context to use for interpreation of nodes in the list node.

        Returns:
            Number or List[Number]: The result(s) of the statements.
        """
        returnNodes = map(lambda element: ReturnNode == type(element), node.elementNodes)
        returnPresent: Number = reduce(add, returnNodes, 0)                 # Are there any nodes that really flush something?
        
        def visitElement(elementNode):
            if not returnPresent:
                return visit(elementNode, context)
            elif type(elementNode) == ReturnNode:
                return visit(elementNode, context)
            visit(elementNode, context)

        elements: List[Number] = []
        elements = list(chain(*map(lambda node: [*elements, visitElement(node)], node.elementNodes)))
        elements = list(filter(partial(is_not, None), elements))            # Filter all None values. Note that None is equal to 0, so is_not is used.
        
        if len(elements) == 1:
            return elements[0]
        return elements

    # visitReturnNode :: ReturnNode -> Context -> Number | Nothing
    def visitReturnNode(node : ReturnNode, context : Context) -> Optional[Number]:
        """ Interpret return 
        Returns the result of interpretation of the node to return when there's
        one present.

        Parameters:
            node (ReturnNode): The node of which the value should be returned.
            context (Context): The context to use for determining return value.
        """
        if node.nodeToReturn:
            return visit(node.nodeToReturn, context)

    functionName: str = f'visit{type(node).__name__}'                       # Determine name of function to call.
    function = locals()[functionName]                                       # Get function with corresponding name.
    return function(node, context)
