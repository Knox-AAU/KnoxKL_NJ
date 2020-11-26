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
            self.NamespaceShort = list()
            self.NamespaceLong = list()
            self.Ontology = list()
            self.Classes = list()
            self.Relations = list()

            #Parse turtle file
            outputs = ParseFromFile(ev.instance.get_value(ev.instance.ONTOLOGY_FILEPATH))

            #Categorise the output
            for output in outputs:
                #Namespace?
                if output[0] == "prefix":
                    self.NamespaceShort.append(output[1])
                    self.NamespaceLong.append(output[2])
                    continue
                #Ontology?
                if output[2] == "owl:Ontology":
                    self.Ontology.append(output[0])
                    continue
                #Class?
                if output[2] == "owl:Class":
                    self.Classes.append(output[0])
                #Relation?
                if output[2] == "owl:ObjectProperty":
                    self.Relations.append(output[0])
        
        def GetNamespaceShort(self):
            return self.NamespaceShort
        
        def GetNamepaceLong(self):
            return self.NamespaceLong
        
        def GetOntology(self):
            return self.Ontology
        
        def GetClasses(self):
            return self.Classes
        
        def GetRelations(self):
            return self.Relations
     
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
    pt = productions.ParseTree(text)
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
