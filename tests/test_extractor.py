from extractor.TripleExtractor import TripleExtractor


class Test:
    extractor = TripleExtractor("da_core_news_lg")

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
    