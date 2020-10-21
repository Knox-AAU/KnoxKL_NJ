from __future__ import annotations
import spacy
#from loader.JsonLoader import NewsStruct, Article
from loader.JsonWrapper import Publication, Article, Paragraph
from rdf.RdfCreator import generate_uri_reference, generate_relation, generate_literal, store_rdf_triples
from rdf.RdfConstants import RelationTypeConstants
from environment.EnvironmentConstants import EnvironmentVariables as ev

nlp = spacy.load("da_core_news_lg")
triples = []
namespace = ev().get_value(ev().KNOX_18_NAMESPACE, "http://www.thisistesturl.example/")
named_individual = []

# Is currently a monster of a function, will split.
def process_publication(publication:Publication):
    """
    Input: 
        A NewsStruct from the loader package.


    Writes entity triples to file
    """
    global triples
    #Extract publication info and adds it to the RDF triples.
    extract_publication(publication)
    for article in publication.articles:
        #For each article, process the text and extract non-textual data in it.
        process_article(article)
        extract_article(article, publication)

    #Function from rdf.RdfCreator, writes triples to file
    store_rdf_triples(triples)

    #Writes named individuals to the output file.
    write_named_individual()

def write_named_individual():
    '''
    Writes each named individual to the file.
    '''
    global named_individual

    #Output file path
    file_path = ev().get_value(ev().OUTPUT_DIRECTORY) + ev().get_value(ev().OUTPUT_FILE_NAME) + ".ttl"

    #Write each named individual to file
    form = "knox:{0} a owl:NamedIndividual, knox:{1} ."
    with open(file_path, "a", encoding="utf-8") as stream:
        for prop1, prop2 in named_individual:
            prop = form.format(prop1, prop2)
            stream.write(prop + "\n")

def add_named_individual(prop_1, prop_2):
    '''
    Adds the named individuals to the named_individual list if it's not already in it.
    '''
    global named_individual
    if [prop_1, prop_2] not in named_individual:
        named_individual.append([prop_1, prop_2])

def extract_publication(pub:Publication):
    global triples
    global namespace

    #Name of a publications publisher
    name = pub.publisher.replace(" ", "_")
    
    #Name of the publication
    pub_name = pub.publication.replace(" ", "_")

    #Adds publication as a named individual
    add_named_individual(pub.publication.replace(" ", "_"), "Publication")
    
    #Add publisher name as data property
    triples.append([
        generate_uri_reference(namespace, ["Publisher"], name),
        generate_relation(RelationTypeConstants.KNOX_NAME),
        generate_literal(name)])

    #Add the "Publisher publishes Publication" relation
    triples.append([
        generate_uri_reference(namespace, ["Publisher"], name),
        generate_relation(RelationTypeConstants.KNOX_PUBLISHES),
        generate_uri_reference(namespace, ["Publication"], pub_name)
    ])
    #Add publication name as data property
    triples.append([
        generate_uri_reference(namespace, ["Publication"], pub_name),
        generate_relation(RelationTypeConstants.KNOX_NAME),
        generate_literal(pub.publication)
    ])


def extract_article(article:Article, publication:Publication):
    '''Input:
        Takes an Article and Publication object from the loader.JsonWrapper package.

        Creates the RDF triples unique to the article.
    '''
    global triples
    namespace = ec().get_value(ec().KNOX_18_NAMESPACE)

    #Creates the article as a named individual
    add_named_individual(str(article.id), "Article")
    #Creates the publisher as a named individual
    add_named_individual(publication.publisher.replace(" ", "_"), "Publisher")
    
    #Adds the Article isPublishedBy Publication relation to the turtle output
    triples.append([
        generate_uri_reference(namespace, ["Article"], str(article.id)),
        generate_relation(RelationTypeConstants.KNOX_IS_PUBLISHED_BY),
        generate_uri_reference(namespace, ["Publisher"], publication.publisher.replace(" ", "_"))
    ])
    

    #Adds the Article knox:Article_Title Title data to the turtle output
    triples.append([
        generate_uri_reference(namespace, ["Article"], str(article.id)),
        generate_relation(RelationTypeConstants.KNOX_ARTICLE_TITLE),
        generate_literal(article.headline)
    ])
    #If the byline exists add the author name to the RDF triples. Author name is required if byline exists.
    if article.byline is not None:
        triples.append([
            generate_uri_reference(namespace, ["Author"], article.byline.name.replace(" ", "_")),
            generate_relation(RelationTypeConstants.KNOX_NAME),
            generate_literal(article.byline.name)
        ])
        #Creates the author as a named individual
        add_named_individual(article.byline.name.replace(" ", "_"), "Author")
        
        #Adds the Article isWrittenBy Author relation to the triples list
        triples.append([
            generate_uri_reference(namespace, ["Article"], str(article.id)),
            generate_relation(RelationTypeConstants.KNOX_IS_WRITTEN_BY),
            generate_uri_reference(namespace, ["Author"], article.byline.name.replace(" ", "_"))
        ])
        #Since email is not required in the byline, if it exsists: add the authors email as a data property to the author.
        if article.byline.email is not None:
            triples.append([
                generate_uri_reference(namespace, ["Author"], article.byline.name.replace(" ", "_")),
                generate_relation(RelationTypeConstants.KNOX_EMAIL),
                generate_literal(article.byline.email)
            ])
    #Adds the publication date to the article, if it exists.        
    if publication.published_at != "":
        triples.append([
            generate_uri_reference(namespace, ["Article"], str(article.id)),
            generate_relation(RelationTypeConstants.KNOX_PUBLICATION_DATE),
            generate_literal(publication.published_at)
        ])
    #For each file that an article is extracted from, add it to the article as a data property
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
    global namespace
    #Article text is split into multiple paragraph objects in the Json, this is joined into one string.
    content = ''.join(para.value for para in article.paragraphs)
    
    #Does nlp on the text
    article_entities = process_article_text(content)
    
    for pair in article_entities:
        #Ensure formatting of the objects name is compatible, eg. Jens Jensen -> Jens_Jensen
        object_ref = str(pair[0]).replace(" ", "_")

        #Changes spacy labels "ORG", "LOC", "PER" to "Organisation", "Location", "Person"
        object_label = str(pair[1])
        object_label = convert_spacy_label_to_namespace(object_label)

        #Ignore un-added labels
        if object_label == "MISC":
            continue

        #Each entity in article added to the "Article mentions Entity" triples
        _object = generate_uri_reference(namespace, [object_label], object_ref)
        _subject = generate_uri_reference(namespace, ["Article"], str(article.id)) 
        relation = generate_relation(RelationTypeConstants.KNOX_MENTIONS)
        
        triples.append([_subject, relation, _object])
        #Each entity given the name data property
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
    #Do nlp
    doc = nlp(article_text)

    #Create article entity from the document entitites
    article_entities = []

    for entities in doc.ents:
        name = entities.text 
        label = entities.label_
        
        #Add entity to list, create it as named individual.
        article_entities.append((name, label))
        if label == "MISC":
            continue
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
