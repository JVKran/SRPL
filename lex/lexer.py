from lex import token

DIGITS = '0123456789'

def check_strings(search_list, input_string):
    return [s.startswith(input_string) for s in search_list]

class Lexer():

    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []
        subclassDict = {}
        token.Token.createSubclassDict(token.Token.__subclasses__(), subclassDict)
        print(subclassDict.keys())

        word = ""
        possible_lexemes = 0

        while self.current_char != None:
            if self.current_char in DIGITS:
                print("Final word:", word)
                word = ""
                self.make_number()
            else:
                word += self.current_char
                print("Running word:", word)
                possible_lexemes = check_strings(subclassDict.keys(), word).count(True)
                print("Amount of lexemes:", possible_lexemes)
                if possible_lexemes == 1 and self.current_char == ' ':
                    print("Final word:", word)
                    word = ""
            if self.current_char == ' ' and possible_lexemes == 0:
                print("Variable:", word)
                word = ""
            self.advance()

        return tokens

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        # print("Number made.")
        if dot_count == 0:
            print("Integer:", int(num_str))
            return
        print("Float:", float(num_str))
