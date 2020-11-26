import productions
import util
from categories import Categories

#1 TurtleDoc
def test_TurtleDoc_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)

    productions.TurtleDoc(testPt)

    assert expected == testPt.root.Size

def test_TurtleDoc_correctWord_statement():
    testString = "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
    expected = 60
    testPt = productions.ParseTree(testString)

    productions.TurtleDoc(testPt)

    assert expected == testPt.root.Size

#4 PrefixID
def test_PrefixID_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixID(testPt, testNode)

    assert expected == actual.Size

def test_PrefixID_correctWord_letters():
    testString = "@prefix abc: <abcd> ."
    expected = 21
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixID(testPt, testNode)

    assert expected == actual.Size

def test_PrefixID_correctWord_letters_spaceSpam():
    testString = "@prefix        abc:      <abcd>       ."
    expected = 39
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixID(testPt, testNode)

    assert expected == actual.Size

def test_PrefixID_wrongWord_letters_missingSpace():
    testString = "@prefixabc: <abcd>."
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixID(testPt, testNode)

    assert expected == actual.Size

def test_PrefixID_wrongWord_letters_missingSpace():
    testString = "@prefix abc:<abcd>."
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixID(testPt, testNode)

    assert expected == actual.Size

def test_PrefixID_wrongWord_letters_missingSpace():
    testString = "@prefixabc:<abcd> ."
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixID(testPt, testNode)

    assert expected == actual.Size

#6 triples
def test_triples_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.triples(testPt, testNode)

    assert expected == actual.Size

def test_triples_correctWord():
    testString = "knox:Link rdf:type owl:DatatypeProperty ; rdfs:domain knox:Article ; rdfs:range xsd:string ."
    expected = 92
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.triples(testPt, testNode)

    assert expected == actual.Size

#7 predicateObjectOneOne
def test_predicateObjectOneOne_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicateObjectListOneOne(testPt, testNode)

    assert expected == actual.Size

def test_predicateObjectOneOne_correctWord():
    testString = "a myNS:person, myNS:person"
    expected = 13
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicateObjectListOneOne(testPt, testNode)

    assert expected == actual.Size

def test_predicateObjectOneOne_correctWord():
    testString = "rdfs:range knox:Location, knox:Person, knox:Date, knox:Organisation ."
    expected = 68
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicateObjectListOneOne(testPt, testNode)

    assert expected == actual.Size
#7 predicateObjectOne
def test_predicateObjectOne_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicateObjectListOne(testPt, testNode)

    assert expected == actual.Size

def test_predicateObjectOne_correctWord():
    testString = "; a myNS:person, myNS:person"
    expected = 28
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicateObjectListOne(testPt, testNode)

    assert expected == actual.Size

#7 predicateObject
def test_predicateObjectList_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicateObjectList(testPt, testNode)

    assert expected == actual.Size

def test_predicateObjectList_correctWord():
    testString = "a myNS:person"
    expected = 13
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicateObjectList(testPt, testNode)

    assert expected == actual.Size

def test_predicateObjectList_correctWord():
    testString = "rdf:type owl:DatatypeProperty ; rdfs:domain knox:Article ; rdfs:range xsd:string ."
    expected = 81
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicateObjectList(testPt, testNode)

    assert expected == actual.Size
    
#8 objectListOne
def test_objectListOne_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.objectListOne(testPt, testNode)

    assert expected == actual.Size

def test_objectListOne_corrrectWord():
    testString = ", myNS:person"
    expected = 13
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.objectListOne(testPt, testNode)

    assert expected == actual.Size

#8 objectList
def test_objectList_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.objectList(testPt, testNode)

    assert expected == actual.Size

def test_objectList_corrrectWord():
    testString = "myNS:person, myNS:person"
    expected = 24
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.objectList(testPt, testNode)

    assert expected == actual.Size

def test_objectList_corrrectWord():
    testString = "myNS:person , myNS:person"
    expected = 25
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.objectList(testPt, testNode)

    assert expected == actual.Size

def test_objectList_corrrectWord():
    testString = "knox:Location, knox:Person, knox:Date, knox:Organisation ."
    expected = 57
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.objectList(testPt, testNode)

    assert expected == actual.Size
    
#9 verb
def test_verb_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.verb(testPt, testNode)

    assert expected == actual.Size

def test_verb_correctWord_predicate():
    testString = "<myfolder/myclasses/person>"
    expected = 27
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.verb(testPt, testNode)

    assert expected == actual.Size

def test_verb_correctWord_a():
    testString = "a"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.verb(testPt, testNode)

    assert expected == actual.Size

def test_verb_wrongWord():
    testString = "abcdefg"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.verb(testPt, testNode)

    assert expected == actual.Size

#10 subject
def test_subject_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.subject(testPt, testNode)

    assert expected == actual.Size

def test_subject_correctWord_IRIREF():
    testString = "<test> a"
    expected = 6
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.subject(testPt, testNode)

    assert expected == actual.Size

def test_subject_correctWord_PNAME_LN_a():
    testString = "myNS:person a"
    expected = 11
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.subject(testPt, testNode)

    assert expected == actual.Size

def test_subject_correctWord_PNAME_LN_rdfType():
    testString = "knox:publishes rdf:type"
    expected = 14
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.subject(testPt, testNode)

    assert expected == actual.Size

#11 predicate
def test_predicate_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicate(testPt, testNode)

    assert expected == actual.Size

def test_predicate_correctWord_IRIREF():
    testString = "<myfolder/myclasses/person>"
    expected = 27
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicate(testPt, testNode)

    assert expected == actual.Size

def test_predicate_correctWord_PrefixedName():
    testString = "myNS:person"
    expected = 11
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicate(testPt, testNode)

    assert expected == actual.Size

def test_predicate_wrongWord_IRIREF_wrongStart():
    testString = "!<myfolder/myclasses/person>"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicate(testPt, testNode)

    assert expected == actual.Size

def test_predicate_wrongWord_IRIREF_wrongEnd():
    testString = "<myfolder/myclasses/person<"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicate(testPt, testNode)

    assert expected == actual.Size

def test_predicate_wrongWord_PrefixedName_wrongStart():
    testString = "!myNS:person"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicate(testPt, testNode)

    assert expected == actual.Size

def test_predicate_wrongWord_PrefixedName_wrongEnd():
    testString = "myNS:person!"
    expected = 11
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.predicate(testPt, testNode)

    assert expected == actual.Size

#12 obj
def test_obj_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.obj(testPt, testNode)

    assert expected == actual.Size

def test_obj_correctWord_iri_PrefixedName():
    testString = "myNS:person"
    expected = 11
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.obj(testPt, testNode)

    assert expected == actual.Size

def test_obj_correctWord_iri_IRIREF():
    testString = "<myfolder/myclasses/person>"
    expected = 27
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.obj(testPt, testNode)

    assert expected == actual.Size

#135s iri
def test_iri_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.iri(testPt, testNode)

    assert expected == actual.Size

def test_iri_correctWord_IRIREF():
    testString = "<myfolder/myclasses/person>"
    expected = 27
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.iri(testPt, testNode)

    assert expected == actual.Size

def test_iri_correctWord_PrefixedName():
    testString = "myNS:person"
    expected = 11
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.iri(testPt, testNode)

    assert expected == actual.Size

def test_iri_wrongWord_IRIREF_wrongStart():
    testString = "!<myfolder/myclasses/person>"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.iri(testPt, testNode)

    assert expected == actual.Size

def test_iri_wrongWord_IRIREF_wrongEnd():
    testString = "<myfolder/myclasses/person<"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.iri(testPt, testNode)

    assert expected == actual.Size

def test_iri_wrongWord_PrefixedName_wrongStart():
    testString = "!myNS:person"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.iri(testPt, testNode)

    assert expected == actual.Size

def test_iri_wrongWord_PrefixedName_wrongEnd():
    testString = "myNS:person!"
    expected = 11
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.iri(testPt, testNode)

    assert expected == actual.Size

#136s PrefixedName
def test_PrefixedName_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixedName(testPt, testNode)

    assert expected == actual.Size

def test_PrefixedName_correctWord_PNAME_LN():
    testString = "myNS:class1"
    expected = 11
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixedName(testPt, testNode)

    assert expected == actual.Size

def test_PrefixedName_correctWord_PNAME_NS():
    testString = "myNS:"
    expected = 5
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixedName(testPt, testNode)

    assert expected == actual.Size

def test_PrefixedName_correctWord_notEOL():
    testString = "myNS:class1 a relation"
    expected = 11
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixedName(testPt, testNode)

    assert expected == actual.Size

def test_PrefixedName_wrongWord():
    testString = "abc"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixedName(testPt, testNode)

    assert expected == actual.Size

def test_PrefixedName_wrongWord_wrongStart():
    testString = "!abc:abc"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PrefixedName(testPt, testNode)

    assert expected == actual.Size