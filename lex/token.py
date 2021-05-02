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
        return self.__class__.__name__ + str(" \'" + str(self.stringToParse) + "\'")

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

class AndToken(Token):
    name = "and"

class OrToken(Token):
    name = "or"

class IfToken(Token):
    name = "if"

class ThenToken(Token):
    name = "then"

class WhileToken(Token):
    name = "while"

class ReturnToken(Token):
    name = "flush"

class VariableToken(Token):
    name = ""

class VariableKeywordToken(Token):
    name = "variable"

class FunctionToken(Token):
    name = "task"

class ExecuteToken(Token):
    name = "execute"

class FunctionStartToken(Token):
    name = "consists_of"

class NewlineToken(Token):
    name = "\n"

class NewlineToken(Token):
    name = ";"

class FunctionEndToken(Token):
    name = "end"

class CommaToken(Token):
    name = ","

class LeftParenToken(Token):
    name = "("

class RightParenToken(Token):
    name = ")"

class IntegerToken(Token):
    name = ""

    def __init__(self, integer : int, lineNumber : int):
        self.stringToParse = int(integer)
        self.lineNumber = lineNumber

    def __new__(cls, stringToParse : str):
        return super(Token, IntegerToken).__new__(IntegerToken)

class FloatToken(Token):
    name = ""

    def __init__(self, value : float, lineNumber : int):
        self.stringToParse = float(value)
        self.lineNumber = lineNumber

    def __new__(cls, stringToParse : str):
        return super(Token, FloatToken).__new__(FloatToken)