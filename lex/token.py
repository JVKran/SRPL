
def createSubclassDict(subclasses, subclassDict):
    if not subclasses:
        return subclassDict
    else: 
        subclassDict.update({subclasses[0].name: subclasses[0]})
        return createSubclassDict(subclasses[1:], subclassDict)


class Token():

    def __init__(self, stringToParse : str, lineNumber : int):
        self.lineNumber = lineNumber
        self.stringToParse = stringToParse

    def __new__(cls, stringToParse : str, lineNumber : int):
        subclassDict = {}
        createSubclassDict(cls.__subclasses__(), subclassDict)
        try:
            subclass = subclassDict[stringToParse]
        except KeyError:
            subclass = VariableToken
        instance = super(Token, subclass).__new__(subclass)
        return instance


class AssignmentToken(Token):
    name = "is"

class VariableToken(Token):
    name = ""
