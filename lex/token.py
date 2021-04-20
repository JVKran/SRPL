
class Token():

    def __init__(self, stringToParse : str, lineNumber : int):
        self.lineNumber = lineNumber
        self.stringToParse = stringToParse

    def __new__(cls, stringToParse : str, lineNumber : int):
        subclassDict = {}
        Token.createSubclassDict(cls.__subclasses__(), subclassDict)
        try:
            subclass = subclassDict[stringToParse]
        except KeyError:
            subclass = VariableToken
        instance = super(Token, subclass).__new__(subclass)
        return instance

    @staticmethod
    def createSubclassDict(subclasses, subclassDict):
        if not subclasses:
            return subclassDict
        else: 
            subclassDict.update({subclasses[0].name: subclasses[0]})
            return Token.createSubclassDict(subclasses[1:], subclassDict)


class AssignmentToken(Token):
    name = "is"

class AddToken(Token):
    name = "plus"

class SubstractToken(Token):
    name = "min"

class DivideToken(Token):
    name = "divided by"

class MultiplyToken(Token):
    name = "multiplied by"

class EqualityToken(Token):
    name = "is equal to"

class NonEqualityToken(Token):
    name = "is not equal to"

class GreaterToken(Token):
    name = "is greater than"

class GreaterEqualToken(Token):
    name = "is greater than or equal to"

class LessToken(Token):
    name = "is less than"

class LessEqualToken(Token):
    name = "is less than or equal to"

class ReturnToken(Token):
    name = "flush"

class VariableToken(Token):
    name = ""