from rdflib import Graph, Literal, URIRef, BNode
from rdflib.namespace import RDFS, OWL, RDF as rdf, XSD
from dotenv import load_dotenv
import os
from RdfConstants import RelationTypeConstants as rConst

def storeRDFTriples(rdfTriples):
    load_dotenv()
    # Get the "graph" in order to contain the rdfTriples
    g = Graph()
    
    for sub, rel, obj in rdfTriples:
        g.add((sub, rel, obj))

    # Bind namespaces to aliases
    g.bind("rdf", rdf)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # Print it
    #print("--------- PRINT THE KNOWLEDGE ---------")
    g.serialize(format="turtle", encoding="utf-8", destination=os.environ.get("RDF_OUTPUT_FOLDER") + "testTurtle")

def createBlankNode():
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
        Exception - If <type> has not been defined in the function
    """
    relType, relValue = relationTypeConstant.split(":")
    if relType == "rdf":
        return rdf.term(relValue)
    if relType == "rdfs":
        return RDFS.term(relValue)

    raise Exception("Relation namespace: " + relType + " not defined in RdfConstants. Input was: " + relationTypeConstant)


load_dotenv()
rdfTriples = [[generateUriReference(os.environ.get("KNOX_18_NAMESPACE"), ["person"], "Bob"), generateRelation(rConst.TYPE), generateUriReference("Object")]]
rdfTriples.append([generateUriReference(os.environ.get("KNOX_18_NAMESPACE"), ["person", "important", "localhero"], "BobTheMan"), generateRelation(rConst.LABEL), generateLiteral("Hero")])
rdfTriples.append([generateUriReference("Test1"), generateRelation(rConst.COMMENT), generateLiteral("COMMENT")])
rdfTriples.append([generateUriReference("Test2"), generateRelation(rConst.PROPERTY), generateLiteral("PROPERTY")])
#[[URIRef(os.environ.get("KNOX_18_NAMESPACE") + "person/Bob"), rdf.term("type"), URIRef("Object")]]
storeRDFTriples(rdfTriples)
#print(dic.lookup(rdfsC.RESOURCE.value))