from lex.token import Token
from typing import TypeVar, Callable, List, Tuple, Optional

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

# createWordList :: String -> [String]
def createWordList(line : str) -> List[str]:
    """ Create list with all words from the passed line. """
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

# readFile :: String -> [String]
def readFile(filename : str) -> List[str]:
    """ Create list with lines in file. """
    file = open(filename, "r")
    text: List[str] = file.read().splitlines(True)          # Create list with all lines, but leave the newline character in place.
    file.close()
    return text

# wordToToken :: Tuple -> Token
def wordToToken(wordAndLine : Tuple) -> Token:
    return Token(*wordAndLine)

# textToTokens :: Callable -> [Token] -> [String] -> [Token]
def textToTokens(f : Callable[[str,int], List[Token]], text : List[str]) -> List[Token]:
    if not text:
        return []
    return textToTokens(f, text[:-1]) + f(text[-1], len(text))

# lineToTokens :: String -> Integer -> [Token]
def lineToTokens(line : str, lineNumber : int) -> List[Token]:
    wordList = createWordList(line)
    wordList = list(filter(lambda x: x != "", wordList))
    lineList = [lineNumber] * len(line)
    wordList = list(zip(wordList, lineList))
    tokenList = list(map(wordToToken, wordList))
    return tokenList

# lex :: String -> String -> [Token]
def lex(text : Optional[str], fileName : Optional[str]) -> List[Token]:
    if text == None:
        text = readFile(fileName)
    tokenList = textToTokens(lineToTokens, text)
    return tokenList
