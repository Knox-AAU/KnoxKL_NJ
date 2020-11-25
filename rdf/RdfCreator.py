from rdflib import Graph, Literal, URIRef, BNode
from rdflib.namespace import NamespaceManager, RDFS, OWL, XSD, RDF as Rdf
from environment.EnvironmentConstants import EnvironmentVariables as ev
import os
from rest.DataRequest import send_triple_to_db
from rdf import KNOX
from requests.exceptions import ConnectionError

def store_rdf_triples(rdfTriples, output_file_name = ev.instance.get_value(ev.instance.OUTPUT_FILE_NAME), 
                destination_folder = ev.instance.get_value(ev.instance.RDF_OUTPUT_FOLDER), 
                output_format = ev.instance.get_value(ev.instance.OUTPUT_FORMAT), endpoint: str = None):
    """
    Input:
        rdfTriples: list of RDF triples with correct type - List containing triples on the form (Subject, RelationPredicate, Object).
        output_file_name: str - The Name of the outputted file
    
    Takes in a list of RDF triples and parse them into a ready RDF format.
    The format and output folder of the files are dependent of the configation of the .env file
    
    """
    # Check if the environment has been set properly, raise error if not
    if output_file_name is None or destination_folder is None or output_format is None:
        err_format = "A Required Environment Variable is undefined[{0}={1}, {2}={3}, {4}={5}]"
        raise EnvironmentError(err_format.format(ev.instance.OUTPUT_FILE_NAME, output_file_name, ev.instance.RDF_OUTPUT_FOLDER, destination_folder, ev.instance.OUTPUT_FORMAT, output_format))

    # Get the "graph" in order to contain the rdfTriples
    # Switch the bad namespacemanager with the good one which do not create prefix'es
    g: Graph = Graph()
    goodManager = KnoxNameSpaceManager(g)
    g.namespace_manager = goodManager
    
    for sub, rel, obj in rdfTriples:
        g.add((sub, rel, obj))
    
    # Check if output folder already exist, create it if not
    if not os.path.exists(os.path.abspath(destination_folder)):
        os.mkdir(os.path.abspath(destination_folder))

    if endpoint is None:
        endpoint = ev.instance.get_value(ev.instance.TRIPLE_DATA_ENDPOINT)

    file_extention = __calculateFileExtention__(output_format)
    g.serialize(format=output_format, encoding="utf-8", destination=destination_folder + output_file_name + file_extention)
    with open(f'{destination_folder}{output_file_name}{file_extention}', 'r', encoding='utf-8') as f:
        content = f.read()
        success = send_triple_to_db(content, endpoint=endpoint)
        if not success:
            print(f'Unable to send file to database', 'error')
            raise ConnectionError('Unable to post to the database')
        print(f'Successfully sent publication <{output_file_name}> to server', 'info')

def generate_blank_node():
    """
    Returns:
        A new instance of RDF class BNode (blank node)

    Creates a blank node for the RDF graph.
    The blank node represents a resource where the URI or Literal is unknown or hasn't been given.
    By the RDF standard a blank node can only be used as the subject or object in an RDF triple.
    """
    return BNode()

def generate_literal(value):
    """
    Input:
        value: A Python primitive type - The value to be associated with the resulting RDF Literal Node for the graph
    Returns:
        A new instance of RDF class Literal, with literal value and type based on value:
    
    Takes in a value and creates a RDF Literal instance containing the value and associated type.
    """
    return Literal(value)

def generate_uri_reference(namespace, sub_uri_list = [], ref = ""):
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

def generate_relation(relationTypeConstant):
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
    elif relType == "knox":
        return KNOX.term(relValue)
    else:
        raise Exception("Relation namespace: " + relType + " not defined in RdfConstants. Input was: " + relationTypeConstant)

def __calculateFileExtention__(format):
    """
    Inputs:
        format: str - The format in which the file generated by the RDF triples are to be saved
    Returns:
        str - The file extension associated with the format. "" (empty string) if a matching format could not be found
    
    Calculates the file extension for the given format
    """
    switch = {
        "turtle": ".ttl",
        "html": ".html",
        "hturtle": ".ttl",
        "mdata": ".IVD",
        "microdata": ".IVD",
        "n3": ".n3",
        "nquads": ".nq",
        "nt": ".nt",
        "rdfa": ".xml",
        "rdfa1.0": ".xml",
        "rdfa1.1": ".xml",
        "trix": ".xml",
        "xml": ".xml"}
    
    return switch.get(format, "")

class KnoxNameSpaceManager(NamespaceManager):
    """
    An override of rdflib built-in NamespaceManager.
    This is used in order to escape the default prefix'es being added to the output
    """

    def __init__(self, graph):
        self.graph = graph
        self.__cache = {}
        self.__cache_strict = {}
        self.__log = None
        self.__strie = {}
        self.__trie = {}
        for p, n in self.namespaces():  # self.bind is not always called
            insert_trie(self.__trie, str(n))
