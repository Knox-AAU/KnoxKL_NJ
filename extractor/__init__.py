from __future__ import annotations
import spacy
from loader.JsonLoader import NewsStruct, Article, Publication

nlp = spacy.load("da_core_news_lg")

# Is currently a monster of a function, will split.
def process_publication(news_struct:NewsStruct):
    """
    Input: 
        A NewsStruct from the loader package.

    Returns: 

    """
    
    

    pass

def process_article_text(article_text:str):
    """
    Input:
        Takes a string
    Returns:
        A list of "string" and label pairs. Eg: [("Jens Jensen", Person), ...]
    
    Runs the article text through the spacy pipeline
    """
    doc = nlp(article_text)

    article_entities = []

    for entitites in doc.ent:
        article_entities.append(entitites)

    return article_entities

