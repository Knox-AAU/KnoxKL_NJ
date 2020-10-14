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
    global triples
    for pub in news_struct.publications:
        extract_publication(pub)
        for article in pub.articles:
            process_article(article)
            extract_article(article, pub)



    
    store_rdf_triples(triples)

    # Entity linking
    create_named_individual()
    pass

def extract_publication(pub:Publication):
    global triples

    pass

def create_named_individual():
    global triples
    #Creating named individual
    file_path = ec().get_value(ec().OUTPUT_DIRECTORY) + ec().get_value(ec().OUTPUT_FILE_NAME) + ".ttl"
    with open(file_path, "a", encoding="utf-8") as stream:
        for sub, _, obj in triples:
            if "/" in obj:
                ref = obj.split("/")
                form = "knox:{0} a owl:NamedIndividual, knox:{1} ."
                named_individual = form.format(ref[-1], ref[-2]) 
                stream.writelines(named_individual + "\n")
            if "/" in sub:
                ref = sub.split("/")
                form = "knox:{0} a owl:NamedIndividual, knox:{1} ."
                named_individual = form.format(ref[-1], ref[-2]) 
                stream.writelines(named_individual + "\n")

def extract_article(article:Article, publication:Publication):
    namespace = ec().get_value(ec().KNOX_18_NAMESPACE)
    global triples

    triples.append([generate_uri_reference(namespace, ["Article"], article.nmId), generate_relation(RelationTypeConstants.KNOX_IS_PUBLISHED_BY), generate_uri_reference(namespace, ["Publisher"], publication.publisher)])
    triples.append([generate_uri_reference(namespace, ["Article"], article.nmId), generate_relation(RelationTypeConstants.KNOX_IS_WRITTEN_BY), generate_uri_reference(namespace, ["Author"], article.authorName.replace(" ", "_"))])
    triples.append([generate_uri_reference(namespace, ["Article"], article.nmId), generate_relation(RelationTypeConstants.KNOX_ARTICLE_TITLE), generate_literal(article.title)])
    
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


        #Ensure formatting of the objects name is compatible, eg. Jens Jensen -> Jens_Jensen
        object_ref = str(pair[0]).replace(" ", "_")

        #Changes spacy labels "ORG", "LOC", "PER" to "Organisation", "Location", "Person"
        object_label = str(pair[1])
        object_label = convert_spacy_label_to_namespace(object_label)

        if object_label == "MISC":
            continue
        _object = generate_uri_reference(namespace, [object_label], object_ref)
        _subject = generate_uri_reference(namespace, ["Article"], article.nmId) 
        relation = generate_relation(RelationTypeConstants.KNOX_MENTIONS)

        triples.append([_subject, relation, _object])
    

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

def convert_spacy_label_to_namespace(string:str):
    """
    Input:
        A string matching a spacy label
    Returns:
        A string matching a class in the ontology.
    """
    if string == "PER":
            string = string.replace("PER", "Person")
    elif string == "ORG":
            string = string.replace("ORG", "Organisation")
    elif string == "LOC":
            string = string.replace("LOC", "Location")

    return string