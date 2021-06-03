# SPDX-FileCopyrightText: © 2021 Jochem van Kranenburg <jochem.vankranenburg@outlook.com>
# PDX-License-Identifier: AGPL-3.0 License

from typing import List, Dict

class Token():

    # __init__ :: String -> Integer -> Nothing
    def __init__(self, stringToParse: str, lineNumber: int) -> None:
        self.stringToParse = stringToParse
        self.lineNumber = lineNumber

    # __new__ :: Token -> String -> Integer -> Token
    def __new__(cls: 'Token', stringToParse: str, lineNumber: int) -> 'Token':
        """ Create new token.
        This method might need some more explanation too. First of all, 
        a subclass dictionary is created. This dictionary contains the
        names (for example if, while, \n, plus, etc.) and the corresponding
        subclass.

        This way, a lexed word can easily be used to create an instance 
        of the corresponding subclass. 

        Parameters:
            stringToParse (str): The string to convert to a token.
            lineNumber (int): The number of the line in the file at which the word is located.
        """
        subclassDict: Dict[str, 'Token'] = {}
        cls.createSubclassDict(cls.__subclasses__(), subclassDict)
        if stringToParse and stringToParse[0].isdigit():
            if '.' in stringToParse:
                subclass = FloatToken
            else:
                subclass = IntegerToken
        elif stringToParse == '\n':
            subclass = NewlineToken
        else:
            try:
                subclass = subclassDict[stringToParse]
            except KeyError:
                subclass = VariableToken
        return super(cls, subclass).__new__(subclass)

    @staticmethod
    # createSubclassDict :: [Token] -> Dictionary -> Dictionary
    def createSubclassDict(subclasses: List['Token'], subclassDict: Dict[str, 'Token']) -> Dict[str, 'Token']:
        """ Create subclass dictionary
        This method returns a dictionary with the names (such as 'is', 'divided_by', etc.) as keys
        and the subclass type as values. This dictionary can then be used for easy instantiation
        of tokens.

        Parameters:
            subclasses (List): A list with all subclasses.
            subclassDict (Dict): The constantly updated dictionary until all subclasses have been added.

        Returns:
            Dict: The dictionary with name and subclass pairs.
        """
        if not subclasses:
            return subclassDict
        else: 
            subclassDict.update({subclasses[0].name: subclasses[0]})
            return Token.createSubclassDict(subclasses[1:], subclassDict)

    # __str__ -> String
    def __str__(self) -> str:
        return self.__class__.__name__ + str(" \'" + str(self.stringToParse) + "\'")

    # __repr__ -> String
    def __repr__(self) -> str:
        return str(self)

class IntegerToken(Token):
    name = ""

    # __init__ :: Integer -> Integer -> Nothing
    def __init__(self, integer: int, lineNumber: int) -> None:
        self.stringToParse = int(integer)
        self.lineNumber = lineNumber

    # __new__ :: Token -> String -> IntegerToken
    def __new__(cls: Token, stringToParse: str) -> 'IntegerToken':
        return super(cls, IntegerToken).__new__(IntegerToken)

class FloatToken(Token):
    name = ""

    # __init__ :: Float -> Integer -> Nothing
    def __init__(self, value: float, lineNumber: int) -> None:
        self.stringToParse = float(value)
        self.lineNumber = lineNumber

    # __new__ :: Token -> String -> FloatToken
    def __new__(cls: Token, stringToParse: str) -> 'FloatToken':
        return super(cls, FloatToken).__new__(FloatToken)

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

class ElseToken(Token):
    name = "else"

class WhileToken(Token):
    name = "while"

class ForToken(Token):
    name = "for"

class ToToken(Token):
    name = "to"

class StepToken(Token):
    name = "step"

class ReturnToken(Token):
    name = "flush"

class VariableToken(Token):
    name = ""

class VariableKeywordToken(Token):
    name = "variable"

class FunctionToken(Token):
    name = "task"

class FunctionParameterToken(Token):
    name = "with"

class ExecuteToken(Token):
    name = "execute"

class NowToken(Token):
    name = "now"

class FunctionStartToken(Token):
    name = "contains"

class NewlineToken(Token):
    name = "\n"

class NewlineToken(Token):
    name = ";"

class FunctionEndToken(Token):
    name = "end"

class CommaToken(Token):
    name = "&"

class LeftParenToken(Token):
    name = "("

class RightParenToken(Token):
    name = ")"
