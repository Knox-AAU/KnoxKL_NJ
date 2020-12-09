import turtleParser.productions as productions
import turtleParser.util as util
import turtleParser.turtleExtractor as turtleExtractor
from turtleParser.categories import Categories
from environment.EnvironmentConstants import EnvironmentVariables as ev

class RuntimeOntology:
    """
    The singleton Environment wrapper for the inner class
    """
    class __RuntimeOntology:
        """
        The inner classe with only one instance
        """
        def __init__(self):
            self.Namespaces = list()        #["@prefix", "knox:", "<iri>"]
            self.OntologyNamespace = list() #["knox:, "rdf:type", "owl:Ontology"]
            self.Classes = list()           #[knox:Person, "a", "owl:Class"]
            self.ObjectProperties = list()  #[knox:isWrittenBy, "rdf:type", "owl:ObjectProperty"]
            self.DataProperties = list()    #[knox:Email, "a", "owl:DatatypeProperty"]

            #Parse turtle file
            outputs = ParseFromFile(ev.instance.get_value(ev.instance.ONTOLOGY_FILEPATH, ".ontology.ttl") )

            #Categorise the output
            for output in outputs:
                #Namespace?
                if output[0] == "@prefix":
                    self.Namespaces.append(output)
                    continue
                
                #Ontology?
                if output[2] == "owl:Ontology":
                    self.OntologyNamespace.append(output[0])
                    continue
                #Class?
                if output[2] == "owl:Class":
                    self.Classes.append(output[0])

                #Object Property (relation)?
                if output[2] == "owl:ObjectProperty":
                    self.ObjectProperties.append(output)

                #Datatype Property (relation)?
                if output[2] == "owl:DatatypeProperty":
                    self.DataProperties.append(output)
        
        def GetNamespaceShort(self):
            return self.NamespaceShort
        
        def GetNamepaceLong(self):
            return self.NamespaceLong
        
        def GetOntologyNamespace(self):
            '''
            Return:
                string: str - iri of ontology
            '''
            #<IRI> or Prefix:
            string = self.OntologyNamespace[0]

            #If in prefix format (last char is ':'), then convert to IRI
            if string[len(string)-1] == ':':

                string = self.PrefixToIRI(string)

                if string is None:
                    return None

            #Strip '<' and '>'
            string = string.lstrip('<').rstrip('>')

            #Add '/' if it is missing
            if string.endswith('/'):
                return string
            return string + '/'
        
        def GetClasses(self):
            return self.Classes
        
        def GetRelations(self):
            return self.Relations

        def PrefixToIRI(self, prefix):
            '''
                Searches through all namespaces to find and convert a specified prefix.
                Input:
                    NamespaceShort: str - The prefix to be converted.
                Return:
                    NamespaceLong: str - The IRI of that prefix if found.
                                None - if not found.
            '''  
            for namespace in self.Namespaces:
                if namespace[1] == prefix:
                    return namespace[2]                
            return None
    
    instance: __RuntimeOntology = None

    def __new__(cls):
        """
        Overrides __new__ dunder method to return the instance of the inner class each time an object is called.
        This is where the singleton magic is happening
        """
        if not RuntimeOntology.instance:
            RuntimeOntology.instance = RuntimeOntology.__RuntimeOntology()
        return RuntimeOntology.instance

def Parse(text):
    """
    Parses turtle text format
    Input:
        text: str - a turtle(ttl.) string to be parsed
    Return:
        tripleList: list[string, string, string] - All the namespaces, triples and classes
    """
    #Delete Comments
    preproText = util.DeleteComments(text)

    #Parse
    pt = productions.ParseTree(preproText)
    productions.TurtleDoc(pt)

    #Extract namespaces
    tripleList = turtleExtractor.getNameSpaceTriples(pt)
    
    #Extract triples/classes
    triples = turtleExtractor.getTriples(pt)

    #Combine the lists
    for triple in triples:
        tripleList.append(triple)

    #Return namespace and
    return tripleList

def ParseFromFile(filePath):
    return Parse(util.TextFromFilePath(filePath))