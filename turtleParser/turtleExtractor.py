import productions
import util
import turtleExtractor
from categories import Categories

def getNameSpaceTriples(pt):
    prefixTriples = list()

    #Get prefixes
    prefixList = pt.root.getNodesByCategory(Categories.prefixID)
    
    for prefix in prefixList:
        prefixTriple = list()
        
        #Subject (prefix)
        prefixTriple.append("prefix")

        #Predicate (short namespace)
        shortList = prefix.getStringsByCategory(Categories.PNAME_NS)
        if len(shortList) > 0:
            prefixTriple.append(shortList[0])

        #Object (long namespace)
        longList = prefix.getStringsByCategory(Categories.IRIREF)
        if len(longList) > 0:
            prefixTriple.append(longList[0])

        prefixTriples.append(prefixTriple)

    return prefixTriples

def getTriples(pt):
    classTriples = list()

    #Get prefixes
    triples = pt.root.getNodesByCategory(Categories.triples)

    for triple in triples:
        classTriple = list()

        #Subject
        classTriple.append(triple.getStringsByCategory(Categories.subject)[0])

        #Predicate
        classTriple.append(triple.getStringsByCategory(Categories.verb)[0])

        #Object
        classTriple.append(triple.getStringsByCategory(Categories.obj)[0])
        
        classTriples.append(classTriple)   
    return classTriples