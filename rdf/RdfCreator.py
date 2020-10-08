from rdflib import Graph, Literal, URIRef, BNode
from rdflib.namespace import RDFS, OWL, RDF as Rdf, XSD
from environment.EnvironmentConstants import EnvironmentConstants as ec
import os

def storeRDFTriples(rdfTriples, output_file_name = ec().getOutputFileName()):
    """
    Input:
        rdfTriples: list of RDF triples with correct type - List containing triples on the form (Subject, RelationPredicate, Object).
        output_file_name: str - The Name of the outputted file
    
    Takes in a list of RDF triples and parse them into a ready RDF format.
    The format and output folder of the files are dependent of the configation of the .env file
    
    """
    # Get the "graph" in order to contain the rdfTriples
    g = Graph()
    
    for sub, rel, obj in rdfTriples:
        g.add((sub, rel, obj))
    
    # Bind namespaces to aliases
    g.bind("rdf", Rdf)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # Print it
    #print("--------- PRINT THE KNOWLEDGE ---------")
    output_format = ec().getTripleOutputFormat()
    destination_folder = ec().getRDFOutputFolder()
    # Check if output folder already exist, create it if not
    if not os.path.exists(os.path.abspath(destination_folder)):
        os.mkdir(os.path.abspath(destination_folder))
    temp = destination_folder + output_file_name
    g.serialize(format=output_format, encoding="utf-8", destination=temp)

def generateBlankNode():
    """
    Returns:
        A new instance of RDF class BNode (blank node)

    Creates a blank node for the RDF graph.
    The blank node represents a resource where the URI or Literal is unknown or hasn't been given.
    By the RDF standard a blank node can only be used as the subject or object in an RDF triple.
    """
    return BNode()

def generateLiteral(value):
    """
    Input:
        value: A Python primitive type - The value to be associated with the resulting RDF Literal Node for the graph
    Returns:
        A new instance of RDF class Literal, with literal value and type based on value:
    
    Takes in a value and creates a RDF Literal instance containing the value and associated type.
    """
    return Literal(value)

def generateUriReference(namespace, sub_uri_list = [], ref = ""):
    """
    Input:
        namespace: str - The base namespace for the resource URL
        sub_uri_list: list - A sorted list of sub uri's from the namespace, used navigating to the correct resource
        ref: str - The resource reference
    Returns:
        An instance of the RDF URIRef class, containing the combined URL for the specified resource
    
    Generates an URI reference to a RDF resource.

    Example of usage:
    To generate the URL resource: http://example.org/person/important/localhero/BobTheMan  
    The following values should be used:  
        namespace: http://example.org/  
        sub_uri_list: ["person", "important", "localhero"]  
        ref: "BobTheMan"  
    """
    reference_str = namespace

    for sub_uri in sub_uri_list:
        reference_str += sub_uri + "/"
    
    reference_str += ref
    return URIRef(reference_str)

def generateRelation(relationTypeConstant):
    """
    Input:
        relationTypeConstants - str - A string formatted in the form of <type>:<name> used in RdfConstants
    Returns:
        A relation predicate for the correct type as specified in relationTypeConstants:
    Raises:
        Exception - If <relationTypeConstant> has not been defined in the function
    """
    relType, relValue = relationTypeConstant.split(":")
    if relType == "rdf":
        return Rdf.term(relValue)
    elif relType == "rdfs":
        return RDFS.term(relValue)
    elif relType == "owl":
        return OWL.term(relValue)
    elif relType == "xsd":
        return XSD.term(relValue)
    else:
        raise Exception("Relation namespace: " + relType + " not defined in RdfConstants. Input was: " + relationTypeConstant)