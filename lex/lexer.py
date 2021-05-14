from lex.token import Token
from typing import TypeVar, Callable, List, Tuple, Optional

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

# createWordList :: String -> [String]
def createWordList(line : str) -> List[str]:
    """ Create list of words
    Converts the passed line to a list with a word at every index.
    
    Parameters:
        line (str): The line to convert into a list of words.
        
    Returns:
        List: The list with words of which the line was made out of.
    """
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
    """ Read file into list with lines
    This function reads a file and stores every line at a seperate index.
    Note that every line still has its newline character.

    Parameters:
        filename (str): The name of the file to convert.

    Returns:
        List: The list with a line at each index.
    """
    file = open(filename, "r")
    text: List[str] = file.read().splitlines(True)          # Create list with all lines, but leave the newline character in place.
    file.close()
    return text

# wordToToken :: Tuple -> Token
def wordToToken(wordAndLine : Tuple) -> Token:
    return Token(*wordAndLine)

# textToTokens :: Callable -> [Token] -> [String] -> [Token]
def textToTokens(f : Callable[[str,int], List[Token]], text : List[str]) -> List[Token]:
    """ Convert text to tokens
    This function executes the passed callable on every line of the file.

    Parameters:
        f (Callable): The function to execute on every element.
        text (List): The list with lines on which the callable should be executed.

    Returns:
        List: A list with tokens.
    """
    if not text:
        return []
    return textToTokens(f, text[:-1]) + f(text[-1], len(text))

# lineToTokens :: String -> Integer -> [Token]
def lineToTokens(line : str, lineNumber : int) -> List[Token]:
    """ Convert line to tokenlist
    This function converts a line with words to a list with tokens. It delegates
    some work to wordToToken which, as the name suggests, converts a tuple with a
    word and a linenumber to a token.

    Parameters:
        line (str): The line to 'tokenize'.
        lineNumber (int): The number of this line in the original file.

    Returns:
        List: The list with tokens of this specific line.
    """
    wordList = createWordList(line)
    wordList = list(filter(lambda x: x != "", wordList))
    lineList = [lineNumber] * len(line)
    wordList = list(zip(wordList, lineList))
    tokenList = list(map(wordToToken, wordList))
    return tokenList

# lex :: String -> String -> [Token]
def lex(text : Optional[str], fileName : Optional[str]) -> List[Token]:
    """ Lex file or text
    This function lexes a given piece of text or text in the desired file.

    Parameters:
        text (str): The text to lex.
        fileName (str): The name of the file to lex.
    """
    if text == None:
        text = readFile(fileName)
    tokenList = textToTokens(lineToTokens, text)
    return tokenList
