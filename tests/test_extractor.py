import extractor


class Test:
    def test_spacy_conversion(self):
        per_string = "PER"
        org_string = "ORG"
        loc_string = "LOC"

        assert extractor.convert_spacy_label_to_namespace(per_string) == "Person"
        assert extractor.convert_spacy_label_to_namespace(org_string) == "Organisation"
        assert extractor.convert_spacy_label_to_namespace(loc_string) == "Location"
        assert extractor.convert_spacy_label_to_namespace("MISC") == "MISC"

    def test_article_text_processing(self):
        
        text = "Jens Hansen bor i København, hvor Danske Bank har hovedkvarter."

        entities = extractor.process_article_text(text)

        assert ("Jens Hansen", "PER") in entities
        assert ("København", "LOC") in entities
        assert ("Danske Bank", "ORG") in entities
