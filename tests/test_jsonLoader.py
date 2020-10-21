from loader.FileLoader import load_json
from loader.JsonWrapper import Publication, Article, Paragraph
import os

class Test:
    def test_load_json_constructor_assigns_correct_publication_name(self):
        news = load_json("./tests/data/test_jason.json")

        assert news.publication == "Publication1"
    
    def test_load_publications_should_load_publications_successfully(self):
        news = load_json("./tests/data/test_jason.json")

        assert news.publication is not None

    def test_publication_constructor_assigns_correct_pages_amount(self):
        news = load_json("./tests/data/test_jason.json")
        assert news.pages == 3

    def test_load_json_contains_article_with_correct_text(self):
        news = load_json("./tests/data/test_jason.json")

        assert len(news.articles) > 0
        assert isinstance(news.articles[0], Article)
        assert news.articles[0].headline == 'This is head line'