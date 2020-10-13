from __future__ import annotations
import spacy
from loader.JsonLoader import NewsStruct, Article, Publication
from rdf.RdfCreator import generate_uri_reference, generate_relation, generate_literal, store_rdf_triples
from rdf.RdfConstants import RelationTypeConstants
from environment.EnvironmentConstants import EnvironmentConstants as ec

nlp = spacy.load("da_core_news_lg")
triples = [] 
# Is currently a monster of a function, will split.
def process_publication(news_struct:NewsStruct):
    """
    Input: 
        A NewsStruct from the loader package.


    Writes entity triples to file
    """
    for pub in news_struct.publications:
        for article in pub.articles:

            process_article(article)



    global triples
    store_rdf_triples(triples)

    pass

def process_article(article:Article):
    """
    Input:
        An Article object from the loader package
    Returns:
        A list of triples with subjects, predicates and objects from the article eg. 
        ("Article", "mentions", "Folketinget")
    """
    global triples
    article_entities = process_article_text(article.content)
    namespace = ec().get_value(ec().KNOX_18_NAMESPACE)
    for pair in article_entities:
        _object = generate_uri_reference(namespace, [pair[1]], pair[0])
        _subject = generate_uri_reference(namespace, ["Article"], article.title)
        relation = generate_uri_reference(namespace=namespace, ref="schema#mentions") 
            #generate_relation(RelationTypeConstants.)
        print(_subject)
        print(relation)
        print(_object)
        triples.append(  [_subject, relation, _object])
    
    return triples

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

    for entities in doc.ents:
        name = entities.text 
        label = entities.label_

        article_entities.append((name, label))

    return article_entities

