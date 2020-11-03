from loader.FileLoader import load_json
from loader.JsonWrapper import Publication, Article, Paragraph, Byline
from loader import process_existing
import os
import pytest

xfail = pytest.mark.xfail

class Test:
    path="./tests/data/test_jason.json"
    def test_load_json_constructor_assigns_correct_publication_name(self):
        news = load_json(self.path)

        assert news.publication == "Publication1"
    
    def test_load_publications_should_load_publications_successfully(self):
        news = load_json(self.path)

        assert news.publication is not None

    def test_publication_constructor_assigns_correct_pages_amount(self):
        news = load_json(self.path)
        assert news.pages == 3

    def test_load_json_contains_article_with_correct_text(self):
        news = load_json(self.path)

        assert len(news.articles) > 0
        assert isinstance(news.articles[0], Article)
        assert news.articles[0].headline == 'This is head line'
    
    def test_load_json_articles_contains_correct_amount_of_paragraphs(self):
        news = load_json(self.path)

        assert len(news.articles[0].paragraphs) == 2

    def test_load_json_contains_article_paragraph(self):
        news = load_json(self.path)

        assert news.articles[0].paragraphs[0].kind == "What kind?"
        assert news.articles[0].paragraphs[0].value == "Jens Hansen havde en bondegård."

    def test_load_json_contains_publisher(self):
        news = load_json(self.path)

        assert news.publisher == 'NordJyskePublisher'

    def test_load_json_contains_publishing_date(self):
        news = load_json(self.path)

        assert news.published_at == '2018-03-27T00:00:00+02:00'

    def test_load_json_has_byline_with_content(self):
        news = load_json(self.path)

        assert type(news.articles[0].byline) == Byline
        assert news.articles[0].byline.name == 'Michael Jackson'
        assert news.articles[0].byline.email == 'MJ@king_of_pop.org'
    
    @xfail(strict=True, raises=TypeError)
    def test_load_json_should_error_on_wrong_format(self):
        news = load_json('./tests/data/test_data.json')

    def test_process_existing_should_not_raise_exceptions(self):
        process_existing('./tests/data/', './tests/data/', './tests/data/')