from rdf.RdfCreator import generateBlankNode, generateLiteral, generateUriReference, generateRelation, storeRDFTriples, __calculateFileExtention__
from rdflib import BNode
from rdf.RdfConstants import RelationTypeConstants as rConst
from environment.EnvironmentConstants import EnvironmentConstants as ec
import os
from datetime import datetime

def test_generate_BNode():
    result = generateBlankNode()
    
    assert result != None
    assert isinstance(result, BNode)

def test_generate_literal_number_positive():
    number = 10
    result = generateLiteral(number)

    assert result.isdigit()
    assert result.eq(number)

def test_generate_literal_number_zero():
    number = 0
    result = generateLiteral(number)

    assert result.isdigit()
    assert result.eq(number)

def test_generate_literal_number_negative():
    number = -7
    result = generateLiteral(number)

    try:
        int(result)
    except ValueError:
        assert False
    else:
        assert True
    assert result.eq(number)

def test_generate_literal_string():
    string = "testing"
    result = generateLiteral(string)

    assert result.isidentifier()
    assert result.eq(string)

    string = "10"
    result = generateLiteral(string)

    assert result.isalnum()
    assert result.eq(string)

def test_generate_literal_decimal_positive():
    decimal = 1.5
    result = generateLiteral(decimal)
    
    try:
        float(decimal)
    except ValueError:
        assert False
    else:
        assert True
    assert result.eq(decimal)

def test_generate_literal_decimal_zero():
    decimal = 0.0
    result = generateLiteral(decimal)

    try:
        float(decimal)
    except ValueError:
        assert False
    else:
        assert True
    assert result.eq(decimal)

def test_generate_literal_decimal_negative():
    decimal = -7.92
    result = generateLiteral(decimal)

    try:
        float(result)
    except ValueError:
        assert False
    else:
        assert True

    assert result.eq(decimal)

def test_generate_uri_ref():
    namespace_string = "http://www.example.org/"
    sub_uri_list = ["FirstUri", "SecondUri", "ThridUri"]
    ref_string = "TestRef"

    result = generateUriReference(namespace_string)
    
    assert result.toPython() == namespace_string

    result = generateUriReference(namespace_string, ref=ref_string)
    expected = namespace_string + ref_string
    assert result.toPython() == expected

    result = generateUriReference(namespace_string, sub_uri_list)
    expected = namespace_string + sub_uri_list[0] + "/" + sub_uri_list[1] + "/" + sub_uri_list[2] + "/"
    assert result.toPython() == expected

    result = generateUriReference(namespace_string, sub_uri_list, ref_string)
    expected = expected = namespace_string + sub_uri_list[0] + "/" + sub_uri_list[1] + "/" + sub_uri_list[2] + "/" + ref_string
    assert result.toPython() == expected

def test_generate_relation():
    try:
        generateRelation("badStringFormat")
    except Exception:
        assert True
    else:
        assert False
    
    try:
        generateRelation("flyff:UnknownTypeTest")
    except Exception:
        assert True
    else:
        assert False
    
    test_relation = rConst.RDF_SEQ
    result = generateRelation(test_relation)
    split = test_relation.split(":")

    assert result.toPython().__contains__(split[0])
    assert result.toPython().__contains__(split[1])


def test_store_rdf_triples():
    test_triples = []
    test_triples.append([generateUriReference(ec().getKnox18Namespace(), ["person"], "Bob"), generateRelation(rConst.RDF_TYPE), generateUriReference("Object")])
    test_triples.append([generateUriReference(ec().getKnox18Namespace(), ["person", "important", "localhero"], "BobTheMan"), generateRelation(rConst.RDFS_LABEL), generateLiteral("Hero")])
    test_triples.append([generateUriReference("Test1"), generateRelation(rConst.RDFS_COMMENT), generateLiteral("COMMENT")])
    test_triples.append([generateUriReference("Test2"), generateRelation(rConst.RDF_PROPERTY), generateLiteral("PROPERTY")])
    test_triples.append([generateUriReference("TestOwl"), generateRelation(rConst.OWL_INVERSE_OF), generateLiteral(10)])
    test_triples.append([generateUriReference("TestXSD"), generateRelation(rConst.XSD_DATE_TIME), generateLiteral(datetime.now())])

    output_path = ec().getRDFOutputFolder()
    file_name = "TesterFilexyzwasd"

    try:
        storeRDFTriples(test_triples, file_name)
    except Exception:
        assert False
    else:
        assert True
    
    expected_path = os.path.abspath(output_path + file_name + ".ttl") 
    assert os.path.exists(expected_path)
    assert os.path.isfile(expected_path)

    # Clean up
    if os.path.exists(expected_path):
        os.remove(expected_path)

def test_calculate_file_extension():
    format = "turtle"
    expected = ".ttl"
    result = __calculateFileExtention__(format)

    assert result.__eq__(expected)

    format = "flah"
    expected = ""
    result = __calculateFileExtention__(format)

    assert result.__eq__(expected)