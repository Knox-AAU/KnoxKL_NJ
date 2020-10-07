from loader import JsonLoader
from loader.JsonLoader import NewsStruct
from loader.JsonLoader import Article
import os

class Test:
    def test_newsstruct_constructor_assigns_json_value(self):
        news = NewsStruct("./tests/data/test_data.json")

        assert news.__json__ is not None
        assert int(news.__json__[0]['content']['page']) == 1
    
    def test_load_publications_should_load_publications_successfully(self):
        news = NewsStruct("./tests/data/test_data.json")
        news.load_publications()

        assert "Aalborg" in news.__raw_articles__.keys()
        assert "Thisted_Dagblad" in news.__raw_articles__.keys()

    def test_publication_constructor_assigns_correct_values(self):
        news = NewsStruct("./tests/data/test_data.json")
        news.load_publications()

        assert news.publications[0].publisher == "2._Sektion"
        assert news.publications[0].__article_dicts__[0]['content']['paragraphs'][0]['value'] == "Text from paragraph"

    def test_newsstruct_contains_article_with_correct_text(self):
        news = NewsStruct("./tests/data/test_data.json")
        news.load_publications()

        assert len(news.articles) > 0
        assert isinstance(news.articles[0], Article)
        assert news.articles[0].title == 'sample data title 1'