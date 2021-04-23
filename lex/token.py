from typing import *

class Token():

    def __init__(self, stringToParse : str, lineNumber : int):
        self.stringToParse = stringToParse
        self.lineNumber = lineNumber

    def __new__(cls, stringToParse : str, lineNumber : int):
        subclassDict = {}
        Token.createSubclassDict(cls.__subclasses__(), subclassDict)
        if stringToParse and stringToParse[0].isdigit():
            if '.' in stringToParse:
                subclass = FloatToken
            else:
                subclass = IntegerToken
        else:
            try:
                subclass = subclassDict[stringToParse]
            except KeyError:
                subclass = VariableToken
        instance = super(Token, subclass).__new__(subclass)
        return instance

    @staticmethod
    def createSubclassDict(subclasses : List, subclassDict : Dict) -> Dict:
        if not subclasses:
            return subclassDict
        else: 
            subclassDict.update({subclasses[0].name: subclasses[0]})
            return Token.createSubclassDict(subclasses[1:], subclassDict)

    def __str__(self) -> str:
        return self.__class__.__name__ + str(" \'" + str(self.stringToParse) + "\' at line " + str(self.lineNumber))

    def __repr__(self) -> str:
        return str(self)


class AssignmentToken(Token):
    name = "is"

class AddToken(Token):
    name = "plus"

class SubstractToken(Token):
    name = "min"

class DivideToken(Token):
    name = "divided_by"

class MultiplyToken(Token):
    name = "multiplied_by"

class EqualityToken(Token):
    name = "is_equal_to"

class NonEqualityToken(Token):
    name = "is_not_equal_to"

class GreaterToken(Token):
    name = "is_greater_than"

class GreaterEqualToken(Token):
    name = "is_greater_than_or_equal_to"

class LessToken(Token):
    name = "is_less_than"

class LessEqualToken(Token):
    name = "is_less_than_or_equal_to"

class ReturnToken(Token):
    name = "flush"

class VariableToken(Token):
    name = ""

class FunctionToken(Token):
    name = "task"

class FunctionStartToken(Token):
    name = "consists_of"

class IntegerToken(Token):
    name = ""

    def __init__(self, integer : int, lineNumber : int):
        self.stringToParse = integer
        self.lineNumber = lineNumber

    def __new__(cls, stringToParse : str):
        return super(Token, IntegerToken).__new__(IntegerToken)

class FloatToken(Token):
    name = ""

    def __init__(self, float : float, lineNumber : int):
        self.stringToParse = float
        self.lineNumber = lineNumber

    def __new__(cls, stringToParse : str):
        return super(Token, FloatToken).__new__(FloatToken)