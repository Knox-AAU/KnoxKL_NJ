from __future__ import annotations
import spacy
#from loader.JsonLoader import NewsStruct, Article
from loader.JsonWrapper import Publication, Article, Paragraph
from rdf.RdfCreator import generate_uri_reference, generate_relation, generate_literal, store_rdf_triples
from rdf.RdfConstants import RelationTypeConstants
from environment.EnvironmentConstants import EnvironmentConstants as ec

nlp = spacy.load("da_core_news_lg")
triples = []
property_triples = []
# Is currently a monster of a function, will split.
def process_publication(publication:Publication):
    """
    Input: 
        A NewsStruct from the loader package.


    Writes entity triples to file
    """
    global triples
    extract_publication(publication)
    for article in publication.articles:
        process_article(article)
        extract_article(article, publication)

    
    store_rdf_triples(triples)

    # Entity linking
    #create_named_individual()

    write_named_individual()

def write_named_individual():
    global property_triples
    file_path = ec().get_value(ec().OUTPUT_DIRECTORY) + ec().get_value(ec().OUTPUT_FILE_NAME) + ".ttl"

    form = "knox:{0} a owl:NamedIndividual, knox:{1} ."
    with open(file_path, "a", encoding="utf-8") as stream:
        for prop1, prop2 in property_triples:
            prop = form.format(prop1, prop2)
            stream.write(prop + "\n")
            
    """
    processed_individuals = []
    with open(file_path, "a", encoding="utf-8") as stream:
        for name, label in article_entities:
            if name not in processed_individuals:
                full_label = convert_spacy_label_to_namespace(label)
                form = "knox:{0} a owl:NamedIndividual, knox:{1} ."
                named_individual = form.format(name.replace(" ", "_"), full_label)
                stream.writelines(named_individual + "\n")
                processed_individuals.append(name)
    """

def add_named_individual(prop_1, prop_2):
    global property_triples
    if [prop_1, prop_2] not in property_triples:
        property_triples.append([prop_1, prop_2])

def extract_publication(pub:Publication):
    global triples
    name = pub.publisher
    namespace = ec().get_value(ec().KNOX_18_NAMESPACE)
    triples.append([
        generate_uri_reference(namespace, ["Publisher"], name),
        generate_relation(RelationTypeConstants.KNOX_NAME),
        generate_literal(name)])
    triples.append([
        generate_uri_reference(namespace, ["Publisher"], name),
        generate_relation(RelationTypeConstants.KNOX_PUBLISHES),
        generate_uri_reference(namespace, ["Publication"], pub.publication)
    ])
    add_named_individual(pub.publication.replace(" ", "_"), "Publication")
    triples.append([
        generate_uri_reference(namespace, ["Publication"], pub.publication),
        generate_relation(RelationTypeConstants.KNOX_NAME),
        generate_literal(pub.publication)
    ])


def extract_article(article:Article, publication:Publication):
    namespace = ec().get_value(ec().KNOX_18_NAMESPACE)

    add_named_individual(str(article.id), "Article")
    global triples
    #Adds the Article isPublishedBy Publication relation to the turtle output
    triples.append([
        generate_uri_reference(namespace, ["Article"], str(article.id)),
        generate_relation(RelationTypeConstants.KNOX_IS_PUBLISHED_BY),
        generate_uri_reference(namespace, ["Publisher"], publication.publisher)
    ])
    
    add_named_individual(publication.publisher, "Publisher")
    #Adds the Article knox:Article_Title Title data to the turtle output
    triples.append([
        generate_uri_reference(namespace, ["Article"], str(article.id)),
        generate_relation(RelationTypeConstants.KNOX_ARTICLE_TITLE),
        generate_literal(article.headline)
    ])
    if article.byline is not None:
        triples.append([
            generate_uri_reference(namespace, ["Author"], article.byline.name.replace(" ", "_")),
            generate_relation(RelationTypeConstants.KNOX_NAME),
            generate_literal(article.byline.name)
        ])

        add_named_individual(article.byline.name.replace(" ", "_"), "Author")
        
        #Adds the Article isWrittenBy Author relation to the turtle output
        triples.append([
            generate_uri_reference(namespace, ["Article"], str(article.id)),
            generate_relation(RelationTypeConstants.KNOX_IS_WRITTEN_BY),
            generate_uri_reference(namespace, ["Author"], article.byline.name.replace(" ", "_"))
        ])
    
        if article.byline.email is not None:
            triples.append([
                generate_uri_reference(namespace, ["Author"], article.byline.name.replace(" ", "_")),
                generate_relation(RelationTypeConstants.KNOX_EMAIL),
                generate_literal(article.byline.email)
            ])
    if publication.published_at != "":
        triples.append([
            generate_uri_reference(namespace, ["Article"], str(article.id)),
            generate_relation(RelationTypeConstants.KNOX_PUBLICATION_DATE),
            generate_literal(publication.published_at)
        ])
    if len(article.extracted_from) > 0:
        for ocr_file in article.extracted_from:
            triples.append([
                generate_uri_reference(namespace, ["Article"], str(article.id)),
                generate_relation(RelationTypeConstants.KNOX_LINK),
                generate_literal(ocr_file)
            ])
def process_article(article:Article):
    """
    Input:
        An Article object from the loader package
    Returns:
        A list of triples with subjects, predicates and objects from the article eg. 
        ("Article", "mentions", "Folketinget")
    """
    global triples

    content = ''.join(para.value for para in article.paragraphs)
    
    
    article_entities = process_article_text(content)
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
        _subject = generate_uri_reference(namespace, ["Article"], str(article.id)) 
        relation = generate_relation(RelationTypeConstants.KNOX_MENTIONS)
        
        triples.append([_subject, relation, _object])
        triples.append([_object, generate_relation(RelationTypeConstants.KNOX_NAME), generate_literal(pair[0])])
    

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
        add_named_individual(name.replace(" ", "_"), convert_spacy_label_to_namespace(label))

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