from loader import JsonLoader
from loader.JsonLoader import NewsStruct
import os

class Test:
    def test_newsstruct_constructor_assigns_json_value(self):
        news = NewsStruct("./tests/data/2018-03-27.json")

        assert news.__json__ is not None
        assert int(news.__json__[0]['content']['page']) == 1
    
    def test_load_publications_should_load_publications_successfully(self):
        news = NewsStruct("./tests/data/2018-03-27.json")
        news.load_publications()

        assert "Aalborg" in news.__raw_articles__.keys()
        assert "Thisted_Dagblad" in news.__raw_articles__.keys()

    def test_publication_constructor_assigns_correct_values(self):
        news = NewsStruct("./tests/data/2018-03-27.json")
        news.load_publications()

        assert news.publications[0].publisher == "2._Sektion"