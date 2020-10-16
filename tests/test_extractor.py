import extractor


class Test:
    def test_spacy_conversion(self):
        per_string = "PER"
        org_string = "ORG"
        loc_string = "LOC"

        assert extractor.convert_spacy_label_to_namespace(per_string) == "Person"
        assert extractor.convert_spacy_label_to_namespace(org_string) == "Organisation"
        assert extractor.convert_spacy_label_to_namespace(loc_string) == "Location"

