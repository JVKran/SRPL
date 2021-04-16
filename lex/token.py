
class Token():

    def __init__(self, stringToParse : str, lineNumber : int):
        self.lineNumber = lineNumber
        self.stringToParse = stringToParse

    def __new__(cls, stringToParse : str, lineNumber : int):
        subclass_map = {subclass.name: subclass for subclass in cls.__subclasses__()}
        try:
            subclass = subclass_map[stringToParse]
        except KeyError:
            print("Variable detected!")
            subclass = VariableToken
        instance = super(Token, subclass).__new__(subclass)
        return instance


class AssignmentToken(Token):
    name = "is"

class VariableToken(Token):
    name = ""
