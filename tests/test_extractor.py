from extractor.TripleExtractor import TripleExtractor
from loader.FileLoader import load_json
from environment.EnvironmentConstants import EnvironmentVariables as ev
from rdf.RdfConstants import RelationTypeConstants
from rdf.RdfCreator import generate_uri_reference, generate_relation, generate_literal, store_rdf_triples



class Test:
    extractor = TripleExtractor("da_core_news_lg")
    namespace = ev.instance.get_value(ev.instance.KNOX_18_NAMESPACE, "http://www.thisistesturl.example/")
    publication = load_json("./tests/data/test_jason.json")

    def test_spacy_conversion_to_label(self):
        per_string = "PER"
        org_string = "ORG"
        loc_string = "LOC"

        assert self.extractor.convert_spacy_label_to_namespace(per_string) == "Person"
        assert self.extractor.convert_spacy_label_to_namespace(org_string) == "Organisation"
        assert self.extractor.convert_spacy_label_to_namespace(loc_string) == "Location"
        assert self.extractor.convert_spacy_label_to_namespace("MISC") == "MISC"

    def test_article_text_processing_can_label_entities(self):
        text = "Jens Hansen bor i København, hvor Danske Bank har hovedkvarter."

        entities = self.extractor.process_article_text(text)

        assert ("Jens Hansen", "PER") in entities
        assert ("København", "LOC") in entities
        assert ("Danske Bank", "ORG") in entities

    def test_adding_named_individuals(self):
        
        self.extractor.named_individual.clear()

        assert len(self.extractor.named_individual) == 0

        self.extractor.add_named_individual("Hej med dig", "Jeg hedder Kaj")

        assert len(self.extractor.named_individual) == 1

        self.extractor.named_individual.clear()
    
    def test_extracting_publication_adds_triples(self):

        self.extractor.triples.clear()

        assert len(self.extractor.triples) == 0

        #extract punlication adds three triples to the triples-list
        self.extractor.extract_publication(self.publication)

        assert len(self.extractor.triples) == 3
        assert len(self.extractor.named_individual) == 1

        self.extractor.triples.clear()
        self.extractor.named_individual.clear()

    def test_extract_article(self):
        article = self.publication.articles[0]

        assert len(self.extractor.triples) == 0

        self.extractor.extract_article(article, self.publication)

        assert len(self.extractor.triples) == 8

    def test_write_named_individual(self):
        
        initial_triples_length = len(self.extractor.triples)
        named_individuals = self.extractor.named_individual
        named_individuals_length = len(named_individuals)
        self.extractor.write_named_individual()

        #Each named individual adds two triples to the final triple list.
        assert len(self.extractor.triples) == initial_triples_length + 2*named_individuals_length

        assert named_individuals[0] == ["0", "Article"]
        assert named_individuals[1] == ["NordJyskePublisher", "Publisher"]
        assert named_individuals[2] == ["Michael_Jackson", "Author"]

       
    def test_extractor_with_custom_labels(self):
        extractor2 = TripleExtractor("da_core_news_lg", 
            [["ANI", "Animal"], ["MED", "Media"], ["GAM", "Game"]], 
            [["FOR", "Forbidden"]])

        ani_string = "ANI"
        med_string = "MED"
        gam_string = "GAM"
        for_string = "FOR"

        assert extractor2.convert_spacy_label_to_namespace(ani_string) == "Animal"
        assert extractor2.convert_spacy_label_to_namespace(med_string) == "Media"
        assert extractor2.convert_spacy_label_to_namespace(gam_string) == "Game"
        assert extractor2.convert_spacy_label_to_namespace(for_string) == "FOR"

    def test_process_article(self):
        article = self.publication.articles[1]

        self.extractor.triples.clear()
        self.extractor.named_individual.clear()
        self.extractor.process_article(article)

        _object = generate_uri_reference(self.namespace, ["Location"], "Aalborg")
        _subject = generate_uri_reference(self.namespace, ["Article"], str(1))
        relation = generate_relation(RelationTypeConstants.KNOX_MENTIONS)

        assert [_subject, relation, _object] in self.extractor.triples
        assert [
            _object,
            generate_relation(RelationTypeConstants.KNOX_NAME),
            generate_literal("Aalborg")] in self.extractor.triples
    
    def test_process_article_with_preprocessing(self):
        article = self.publication.articles[1]

        self.extractor.triples.clear()
        self.extractor.named_individual.clear()
        self.extractor.process_article(article, True)

        _object = generate_uri_reference(self.namespace, ["Location"], "Ålborg")
        _subject = generate_uri_reference(self.namespace, ["Article"], str(1))
        relation = generate_relation(RelationTypeConstants.KNOX_MENTIONS)

        assert [_subject, relation, _object] in self.extractor.triples
        assert [_object, generate_relation(RelationTypeConstants.KNOX_NAME), generate_literal('Ålborg')] in self.extractor.triples

        
    def test_process_publication(self):
        self.extractor.triples.clear()
        self.extractor.named_individual.clear()
        try:
            self.extractor.process_publication(self.publication)
        except EnvironmentError:
            pass # Pass Environment Errors as this is because there are missing Environment Variables on the test server     
        assert len(self.extractor.triples) == 42
