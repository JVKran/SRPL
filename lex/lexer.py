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
                if word != " ":
                    print("Final word:", word)
                    word = ""
                self.make_number()
            else:
                word += self.current_char
                # print("Running word:", word)
                possible_lexemes = check_strings(subclassDict.keys(), word).count(True)
                lexeme_index = 0
                if possible_lexemes == 1:
                    lexeme_index = check_strings(subclassDict.keys(), word).index(True)
                # print("Amount of lexemes:", possible_lexemes)
                # print("Length of lexeme: ", len(list(subclassDict.keys())[lexeme_index]))
                # print("Length of word:", len(word))
                if possible_lexemes == 1 and len(list(subclassDict.keys())[lexeme_index]) == len(word) and word != " ":
                    print("Final word:", word)
                    word = ""
                elif self.current_char == ' ' and possible_lexemes == 0 and word != " ":
                    print("Variable:", word)
                    word = ""
                elif possible_lexemes == 0 and ' ' in word:
                    # print("Oh no! We missed a word...", word)
                    tooMuch = word[-1:]
                    word = word[:-2]
                    if word != "":
                        print("Final word:", word)
                    word = tooMuch


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
