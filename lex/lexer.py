from lex.token import Token
from typing import TypeVar, Callable, List, Tuple

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def createWordList(line : str) -> List[str]:
    if not line:
        return [""]
    head, *tail = line
    currentWordList = createWordList(tail)
    if head in " \t\r":
        currentWordList = [""] + currentWordList
    else:
        newWord = head + currentWordList[0]
        currentWordList[0] = newWord
    return currentWordList

def readFile(filename : str) -> List[str]:
    file = open(filename, "r")
    text = file.read().splitlines(True)
    file.close()
    return text

def wordToToken(wordAndLine : Tuple) -> Token:
    return Token(*wordAndLine)

def textToTokens(f : Callable[[str,int], List[Token]], text : List[str]) -> List[Token]:
    if not text:
        return []
    return textToTokens(f, text[:-1]) + f(text[-1], len(text))

def lineToTokens(line : str, lineNumber : int) -> List[Token]:
    wordList = createWordList(line)
    wordList = list(filter(lambda x: x != "", wordList))
    lineList = [lineNumber] * len(line)
    wordList = list(zip(wordList, lineList))
    tokenList = list(map(wordToToken, wordList))
    return tokenList

def lex(text : str, fileName : str) -> List[Token]:
    if text == None:
        text = readFile(fileName)
    tokenList = textToTokens(lineToTokens, text)
    return tokenList
