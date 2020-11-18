import re

from spacy.lang.da.stop_words import STOP_WORDS
import spacy
from typing import OrderedDict

nlp: OrderedDict = None

def remove_stop_words(content: str) -> str:
    """
    Input:
        content: str - A string containing the content that is to have all stop words removed.

    Returns:
        content: str - content without any stop words.

    This function will filter out all danish stopwords (see: https://en.wikipedia.org/wiki/Stop_word)
    Furthermore, commas and periods will be removed, as these are included as stopwords (see: https://ordnet.dk/ddo/ordbog?query=stopord)

    Wiki references have been removed as this methid will be tested using wiki text

    """

    content = re.sub(r'(\[\d+\])|[.,?]', '', content)
    
    # Filter out stopwords
    return_word_list = [i for i in content.split(' ') if i not in STOP_WORDS]
    return ' '.join(word for word in return_word_list)

def convert_to_modern_danish(content: str) -> str:
    """
    Input:
        content: str - A string containing the content that is to be converted to modern Danish.
        

    Throws:
        Exception - If the nlp model provided to the function is not of the danish language.
    
    Returns:
        content: str - input content as a semi-converted string where old spellings are replaced by modern ones.

    This function will convert old danish text to a present version of the text
    This is done with the following conversions:

    aa -> å
    ei -> ej
    ae -> æ
    oe -> ø
    
    Any newline will be converted to a whitespace, and any hyphenation will become a joined word.
    """
    if nlp is None:
        raise Exception("No spaCy model configured.")
    if nlp.lang != 'da':
        raise Exception("Function 'convert_to_modern_danish' requires a danish spaCy model.")

    content = re.sub(r'aa', 'å', content)
    content = re.sub(r'Aa', 'Å', content)
    content = re.sub(r'ei', 'ej', content)
    content = re.sub(r'oe', 'ø', content)
    content = re.sub(r'Oe', 'Ø', content)
    content = re.sub(r'ae', 'æ', content)
    content = re.sub(r'Ae', 'Æ', content)
    content = re.sub(r'\-(\r?)\n','', content)
    content = re.sub(r'\r?\n',' ', content)
    words = [word for word in content.split(' ') if word != '']
    
    for word in words:
        if nlp(word)[0].pos_ == 'NOUN':
            content = content.replace(word, word.lower())

    
    return content