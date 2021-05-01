from lex import token
from typing import TypeVar, Callable, List, Tuple

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

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

def readFile(filename : str) -> List[str]:
    file = open(filename, "r")
    text = file.read().splitlines()
    file.close()
    return text

def wordToToken(wordAndLine : Tuple) -> token.Token:
    return token.Token(*wordAndLine)

def textToTokens(f : Callable[[str,int], List[token.Token]], text : List[str]) -> List[token.Token]:
    if not text:
        return []
    return textToTokens(f, text[:-1]) + f(text[-1], len(text))

def lineToTokens(line : str, lineNumber : int) -> List[token.Token]:
    wordList = createWordList(line)
    lineList = [lineNumber] * len(line)
    wordList = list(zip(wordList, lineList))
    tokenList = list(map(wordToToken, wordList))
    return tokenList

def lex(text : str, fileName : str) -> List[token.Token]:
    if text == None:
        text = readFile(fileName)
    tokenList = textToTokens(lineToTokens, text)
    return tokenList
