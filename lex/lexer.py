from lex import token
from typing import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


def check_strings(search_list, input_string):
    return [s.startswith(input_string) for s in search_list]

def foldl(f: Callable[[A, B], C], base : B, list : List[A]) -> List[C]:
    if not list:
        return base
    head, *tail = list
    return (f(head, foldl(f, base, tail)))

def tupleToToken(x : Tuple[str,int], tail : List[token.Token]) -> List[token.Token]:
    return [token.Token(x[0], x[1])] + tail

def createWordList(line : str) -> List[str]:
    if not line:
        return [""]
    head, *tail = line
    currentWordList = createWordList(tail)
    if head in " \t\n\r":
        currentWordList = [""] + currentWordList
    else:
        newWord = head + currentWordList[0]
        currentWordList[0] = newWord
    return currentWordList

def readFile(filename : str):
    file = open(filename, "r")
    text = file.readlines()
    file.close()
    return text

def wordToToken(word : str):
    return token.Token(word, 1)

def textToTokens(f : Callable[[str,int], List[token.Token]], text : List[str]) -> List[token.Token]:
    if not text:
        return []
    return textToTokens(f, text[:-1]) + f(text[-1], len(text))

def lineToTokens(line : str, lineNumber : int):
    wordList = createWordList(line)
    tokenList = list(map(wordToToken, wordList))
    return tokenList

def lex(fileName : str):
    text = readFile(fileName)
    tokenList = textToTokens(lineToTokens, text)
    return tokenList


class Lexer():

    def __init__(self, filename : str):
        file = open(filename, "r")
        self.text = file.readlines()
        file.close()

        self.pos = -1
        self.lineNumber = 0
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text[self.lineNumber]):
            self.current_char = self.text[self.lineNumber][self.pos]
        elif self.lineNumber < len(self.text) - 1:
            self.lineNumber += 1
            self.pos = 0
            self.current_char = self.text[self.lineNumber][self.pos]
        else:
            self.current_char = None

    def make_tokens(self):
        tokens = []
        subclassDict = {}
        token.Token.createSubclassDict(token.Token.__subclasses__(), subclassDict)

        word = ""
        possible_lexemes = 0

        while self.current_char != None:
            if self.current_char in "\t\n":
                self.advance()
                word = ""
                continue
            if self.current_char.isdigit():
                if word != " ":
                    tokens.append(token.Token(word[:-1], self.lineNumber))
                    word = ""
                tokens.append(self.make_number())
            else:
                word += self.current_char
                possible_lexemes = check_strings(subclassDict.keys(), word).count(True)         # List with True or False for all available lexemes.
                lexeme_index = 0
                if possible_lexemes == 1:
                    lexeme_index = check_strings(subclassDict.keys(), word).index(True)         # Index of first possible lexeme.
                if possible_lexemes == 1 and len(list(subclassDict.keys())[lexeme_index]) == len(word) and word != " ":
                    tokens.append(token.Token(word[:-1], self.lineNumber))
                    word = ""
                elif self.current_char == ' ' and possible_lexemes == 0 and word != " ":
                    tokens.append(token.Token(word[:-1], self.lineNumber))
                    word = ""
                elif possible_lexemes == 0 and ' ' in word:                                     # Read two characters too far; now there are no lexemes anymore.
                    excessCharacters = word[-1:]
                    word = word[:-2]
                    if word != "":
                        tokens.append(token.Token(word[:-1], self.lineNumber))
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
            return token.IntegerToken(int(num_str), self.lineNumber)
        return token.FloatToken(float(num_str), self.lineNumber)
