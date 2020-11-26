import string

def digitList():
    """
    Generates a list of all the digits.
        
    Return:
        digitList: list - A list of numbers from 0 to 9.
    """ 
    digitList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    return digitList

def letterList():
    """
    Generates a list of all letters in the acsii alphabet.
        
    Return:
        letterList: list - A list of letters from a to z and A to Z
    """ 
    letterList = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    return letterList

def StripWhitespacesAndNewlines(string):
    """
    Removes all spaces and newlines from a string
    
    Input:
        string: str - Input string to be stripped from spaces and newlines
    Return:
        stripedString: str - The string that is stripped of spaces and newlines.
    """ 
    #Make array with words, removing whitespaces and so on
    words = string.split()
    stripedString = ''.join(words)
    return stripedString

def TextFromFilePath(filePath):
    """
    Opens a ttl file and extracts all the text that the file contains
    
    Input:
        filePath: str - File path to desired file to be parsed
    Return:
        text: str - The text that the file contains
    """ 

    f=open(filePath, "r")
    if f == None:
        return None
    text = f.read()
    return text