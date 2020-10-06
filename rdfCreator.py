from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, OWL
from dotenv import load_dotenv
import os

def storeRDFTriples(triples):
    load_dotenv()
    # Get the "graph" in order to contain the triples
    g = Graph()
    
    for sub, rel, obj in triples:
        subj = URIRef("http://www.example.org/" + sub)
        g.add((subj, RDF., obj))

    # Bind namespaces to aliases
    g.bind("rdf", RDF)
    g.bind("owl", OWL)

    # Print it
    print("--------- PRINT THE KNOWLEDGE ---------")
    print(os.environ.get("RDF_OUTPUT_FOLDER"))
    print(g.serialize(format="turtle", encoding="utf-8"))