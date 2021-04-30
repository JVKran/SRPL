from lex import token

class Number():

    def __init__(self, value):
        self.value = value

    def add(self, other):
        return Number(self.value + other.value)

    def sub(self, other):
        return Number(self.value - other.value)

    def mul(self, other):
        return Number(self.value * other.value)

    def div(self, other):
        return Number(self.value / other.value)

    def setLineNumber(self, number):
        self.lineNumber = number

    def __repr__(self):
        return str(self.value)


def visit(node):
    function_name = f'visit{type(node).__name__}'
    try:
        function = globals()[function_name]
    except KeyError:
        print(f'No visit{type(node).__name__} defined!')
        return None
    res = function(node)
    return res

def visitOperatorNode(node):
    left = visit(node.left_node)
    right = visit(node.right_node)

    if type(node.operator) == token.AddToken:
        result = left.add(right)
    elif type(node.operator) == token.SubstractToken:
        result = left.sub(right)
    elif type(node.operator) == token.MultiplyToken:
        result = left.mul(right)
    elif type(node.operator) == token.DivideToken:
        result = left.div(right)
    
    # result.setLineNumber(node.token.lineNumber)
    return result

def visitNumberNode(node):
    number = Number(node.token.stringToParse)
    number.setLineNumber(node.token.lineNumber)
    return number

