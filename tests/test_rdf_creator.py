from rdf.RdfCreator import generate_blank_node, generate_literal, generate_uri_reference, generate_relation, store_rdf_triples, __calculateFileExtention__
from rdflib import BNode
from rdf.RdfConstants import RelationTypeConstants as rConst
import os
from datetime import datetime
from requests.exceptions import ConnectionError

class Test:

    
    output_path = './test/output/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    def test_generate_BNode(self):
        result = generate_blank_node()

        assert result != None
        assert isinstance(result, BNode)

    def test_generate_literal_number_positive(self):
        number = 10
        result = generate_literal(number)

        assert result.isdigit()
        assert result.eq(number)

    def test_generate_literal_number_zero(self):
        number = 0
        result = generate_literal(number)

        assert result.isdigit()
        assert result.eq(number)

    def test_generate_literal_number_negative(self):
        number = -7
        result = generate_literal(number)

        try:
            int(result)
        except ValueError:
            assert False
        else:
            assert True
        assert result.eq(number)

    def test_generate_literal_string(self):
        string = "testing"
        result = generate_literal(string)

        assert result.isidentifier()
        assert result.eq(string)

        string = "10"
        result = generate_literal(string)

        assert result.isalnum()
        assert result.eq(string)

    def test_generate_literal_decimal_positive(self):
        decimal = 1.5
        result = generate_literal(decimal)

        try:
            float(decimal)
        except ValueError:
            assert False
        else:
            assert True
        assert result.eq(decimal)

    def test_generate_literal_decimal_zero(self):
        decimal = 0.0
        result = generate_literal(decimal)

        try:
            float(decimal)
        except ValueError:
            assert False
        else:
            assert True
        assert result.eq(decimal)

    def test_generate_literal_decimal_negative(self):
        decimal = -7.92
        result = generate_literal(decimal)

        try:
            float(result)
        except ValueError:
            assert False
        else:
            assert True

        assert result.eq(decimal)

    def test_generate_uri_ref(self):
        namespace_string = "http://www.example.org/"
        sub_uri_list = ["FirstUri", "SecondUri", "ThirdUri"]
        ref_string = "TestRef"

        result = generate_uri_reference(namespace_string)

        assert result.toPython() == namespace_string

        result = generate_uri_reference(namespace_string, ref=ref_string)
        expected = namespace_string + ref_string
        assert result.toPython() == expected

        result = generate_uri_reference(namespace_string, sub_uri_list)
        expected = namespace_string + sub_uri_list[0] + "/" + sub_uri_list[1] + "/" + sub_uri_list[2] + "/"
        assert result.toPython() == expected

        result = generate_uri_reference(namespace_string, sub_uri_list, ref_string)
        expected = expected = namespace_string + sub_uri_list[0] + "/" + sub_uri_list[1] + "/" + sub_uri_list[2] + "/" + ref_string
        assert result.toPython() == expected

    def test_generate_relation(self):
        try:
            generate_relation("badStringFormat")
        except Exception:
            assert True
        else:
            assert False

        try:
            generate_relation("flyff:UnknownTypeTest")
        except Exception:
            assert True
        else:
            assert False

        test_relation = rConst.RDF_SEQ
        result = generate_relation(test_relation)
        split = test_relation.split(":")

        assert result.toPython().__contains__(split[0])
        assert result.toPython().__contains__(split[1])


    def test_store_rdf_triples(self):
        test_triples = self.create_test_triples()

        
        file_name = "TesterFilexyzwasd"

        try:
            store_rdf_triples(test_triples, file_name, self.output_path, 'turtle', 'http://test')
        except ConnectionError:
            assert True
        else:
            assert False

        expected_path = os.path.abspath(self.output_path + file_name + ".ttl") 
        assert os.path.exists(expected_path)
        assert os.path.isfile(expected_path)

        # Clean up
        if os.path.exists(expected_path):
            os.remove(expected_path)

    def test_calculate_file_extension(self):
        format = "turtle"
        expected = ".ttl"
        result = __calculateFileExtention__(format)

        assert result.__eq__(expected)

        format = "flah"
        expected = ""
        result = __calculateFileExtention__(format)

        assert result.__eq__(expected)
    
    def test_no_prefix(self):
        # Create some test data
        test_triples = self.create_test_triples()
        file_name = 'testerfilexyz'
        file_path = self.output_path + file_name + '.ttl'
        prefix_string = '@prefix '

        # Create the output
        try:
            store_rdf_triples(test_triples, file_name, self.output_path, 'turtle', 'http://test')
        except ConnectionError:
            assert True
        else:
            assert False

        # Check output
        output_string = ''
        with open(file_path, 'r', encoding='utf-8') as output:
            output_string = ' '.join(line for line in output.readlines())
        
        index = output_string.find(prefix_string)
        assert index.__eq__(-1)

        # Clean up
        abs_path = os.path.abspath(self.output_path + file_name + ".ttl") 
        if os.path.exists(abs_path):
            os.remove(abs_path)

    def create_test_triples(self):
        test_triples = []
        test_triples.append([generate_uri_reference("knox18", ["person"], "Bob"), generate_relation(rConst.RDF_TYPE), generate_uri_reference("Object")])
        test_triples.append([generate_uri_reference("knox18", ["person", "important", "localhero"], "BobTheMan"), generate_relation(rConst.RDFS_LABEL), generate_literal("Hero")])
        test_triples.append([generate_uri_reference("Test1"), generate_relation(rConst.RDFS_COMMENT), generate_literal("COMMENT")])
        test_triples.append([generate_uri_reference("Test2"), generate_relation(rConst.RDF_PROPERTY), generate_literal("PROPERTY")])
        test_triples.append([generate_uri_reference("TestOwl"), generate_relation(rConst.OWL_INVERSE_OF), generate_literal(10)])
        test_triples.append([generate_uri_reference("TestXSD"), generate_relation(rConst.XSD_DATE_TIME), generate_literal(datetime.now())])

        return test_triples