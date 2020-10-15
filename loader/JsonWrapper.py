from knox_source_data_io.models.model import Model
from typing import List

class Byline:

    name: str
    email: str

    def __init__(self, content: dict = None):

        content = content if content is not None else {}
        self.name = content.get("name", "")
        self.email = content.get("email")

class Paragraph():

    kind: str
    value: str

    def __init__(self, content: dict = None):

        content = content if content is not None else {}
        self.kind = content.get("kind", "")
        self.value = content.get("value", "")



class Article:

    extracted_from: List[str]
    confidence: float
    id: int
    page: int
    headline: str
    subhead: str
    lead: str
    byline: Byline
    paragraphs: list

    def __init__(self, content: dict = None):

        content = content if content is not None else {}
        self.extracted_from = content.get("extracted_from", [])
        self.confidence = content.get("confidence", 0.0)
        self.id = content.get("id", 0)
        self.page = content.get("page", 0)
        self.headline = content.get("headline", "")
        self.subhead = content.get("subhead", "")
        self.lead = content.get("lead", "")
        self.byline = Byline(content.get("byline")) if content.get("byline") is not None else None
        self.paragraphs = []
        temp = content.get("paragraphs", [])
        for val in temp:
            self.paragraphs.append(Paragraph(val))

        

class Publication(Model):

    publication: str
    published_at: str
    publisher: str
    pages: int
    articles: list

    def __init__(self, content: dict = None):

        content = content if content is not None else {}
        self.publication = content.get("publication", "")
        self.published_at = content.get("published_at", "")
        self.publisher = content.get("publisher", "")
        self.pages = content.get("pages", 0)
        self.articles = []
        temp = content.get("articles", [])
        for val in temp:
            self.articles.append(Article(val))