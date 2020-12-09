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

def DeleteComments(text):
    """
    Deletes COMMENTs by scanning for (# (char)* '\\n'). '#' is used in IRIREFs and STRINGs
    
    Input:
        text: str - turtle text
    Return:
        preproText: str - turtle text without comments
    """ 
    preproText = ""
    isCOMMENTInterpolation = False #if true, Look for '\n'
    isIRIREFInterpolation = False #if true, Look for '>'
    isSTRINGInterpolation = False #if true, Look for '"'
    for i in range(len(text)):
        c = text[i]

        #End comment
        if isCOMMENTInterpolation:
            if c == '\n':
                isCOMMENTInterpolation = False
                continue
            continue

        #End iriref
        if isIRIREFInterpolation:
            if c == '>':
                isIRIREFInterpolation = False
                preproText = preproText + c
                continue
            preproText = preproText + c
            continue

        #End string
        if isSTRINGInterpolation:
            if c == '"':
                isSTRINGInterpolation = False
                preproText = preproText + c
                continue
            preproText = preproText + c
            continue

        #Start comment
        if c == '#':
            isCOMMENTInterpolation = True
            continue
            
        #Start iriref
        if c == '<':
            isIRIREFInterpolation = True
            preproText = preproText + c
            continue

        #Start String
        if c == '"':
            isSTRINGInterpolation = True
            preproText = preproText + c
            continue

        preproText = preproText + c
    return preproText