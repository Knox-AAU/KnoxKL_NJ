import productions
import util
import turtleExtractor
from categories import Categories

def Parse(text):
    """
    Parses turtle text format

    Input:
        text: str - a turtle(ttl.) string to be parsed
    Return:
        tripleList: list[string, string, string] - All the namespaces, triples and classes
    """
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

def ParseFromfile(filePath):
    return Parse(util.TextFromFilePath("ttlFiles/testFile.ttl"))
