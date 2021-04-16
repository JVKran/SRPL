
def create_dict(cls, map, index):
    if index >= 0:
        map.update({cls.__subclasses__()[index].name: cls.__subclasses__()[index]})
        return create_dict(cls, map, index - 1)
    else:
        return map

class Token():

    def __init__(self, stringToParse : str, lineNumber : int):
        self.lineNumber = lineNumber
        self.stringToParse = stringToParse

    def __new__(cls, stringToParse : str, lineNumber : int):
        subclass_map = {}
        create_dict(cls, subclass_map, len(cls.__subclasses__()) - 1)
        print(subclass_map)
        try:
            subclass = subclass_map[stringToParse]
        except KeyError:
            subclass = VariableToken
        instance = super(Token, subclass).__new__(subclass)
        return instance


class AssignmentToken(Token):
    name = "is"

class VariableToken(Token):
    name = ""
