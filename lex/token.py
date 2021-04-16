
class Token():

    def __init__(self, stringToParse : str, lineNumber : int):
        self.stringToParse = stringToParse
        self.lineNumber = lineNumber

    def __new__(cls, stringToParse : str, lineNumber : int):
        subclass_map = {subclass.value: subclass for subclass in cls.__subclasses__()}
        subclass = subclass_map[stringToParse]
        instance = super(Token, subclass).__new__(subclass)
        return instance


class AssignmentToken(Token):
    value = "is"



