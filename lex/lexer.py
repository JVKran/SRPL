from lex import token

def check_strings(search_list, input_string):
    return [s.startswith(input_string) for s in search_list]

class Lexer():

    def __init__(self, filename : str):
        file = open(filename,"r")
        self.text = file.readlines()
        file.close()

        self.pos = -1
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.current_char = self.text[0][self.pos] if self.pos < len(self.text[0]) else None

    def make_tokens(self):
        tokens = []
        subclassDict = {}
        token.Token.createSubclassDict(token.Token.__subclasses__(), subclassDict)

        word = ""
        possible_lexemes = 0

        while self.current_char != None:
            if self.current_char.isdigit():
                if word != " ":
                    tokens.append(token.Token(word[:-1], 1))
                    word = ""
                tokens.append(self.make_number())
            else:
                word += self.current_char
                possible_lexemes = check_strings(subclassDict.keys(), word).count(True)         # List with True or False for all available lexemes.
                lexeme_index = 0
                if possible_lexemes == 1:
                    lexeme_index = check_strings(subclassDict.keys(), word).index(True)         # Index of first possible lexeme.
                if possible_lexemes == 1 and len(list(subclassDict.keys())[lexeme_index]) == len(word) and word != " ":
                    tokens.append(token.Token(word[:-1], 1))
                    word = ""
                elif self.current_char == ' ' and possible_lexemes == 0 and word != " ":
                    tokens.append(token.Token(word[:-1], 1))
                    word = ""
                elif possible_lexemes == 0 and ' ' in word:                                     # Read two characters too far; now there are no lexemes anymore.
                    excessCharacters = word[-1:]
                    word = word[:-2]
                    if word != "":
                        tokens.append(token.Token(word[:-1], 1))
                    word = excessCharacters
            self.advance()

        return tokens

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return token.IntegerToken(int(num_str), 1)
        return token.FloatToken(float(num_str), 1)
