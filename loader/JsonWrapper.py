from knox_source_data_io.models.model import Model
from typing import List

class Byline:
    """
    Class structure for containing the byline data from JSON schema: "http://json-schema.org/draft-04/schema#"

    Contains values:
      name - str: The name of the Author of the article
      email - str: The Authors email address
    """
    name: str
    email: str

    def __init__(self, content: dict = None):

        content = content if content is not None else {}
        self.name = content.get("name", "")
        self.email = content.get("email")

class Paragraph():
    """
    Class structure for containing the paragraph data from JSON schema: "http://json-schema.org/draft-04/schema#"

    Contains values:
      kind - str: Describes the paragraph kind
      value - str: The text contained in the paragraph
    """
    kind: str
    value: str

    def __init__(self, content: dict = None):

        content = content if content is not None else {}
        self.kind = content.get("kind", "")
        self.value = content.get("value", "")



class Article:
    """
    Class structure for containing the article data from JSON schema: "http://json-schema.org/draft-04/schema#"

    Contains values:
      extracted_from - List[str]: An array of strings containing the filenames that the article is extracted from 
      confidence - float: A confidence score for the correctness of the article data
      id - int: The id of the article
      page - int: The page number where the article were found
      headline - str: The headline of the article
      subhead - str: The subheader of the article
      lead - str: Unknown at this time
      byline - Byline: Object instance of the byline for the article, describing the Author
      paragraphs - List[Paragraphs]: A list containing the paragraph objects for the article
    """
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
        self.extracted_from = []
        js_extracted_from = content.get("extracted_from", [])
        for val in js_extracted_from:
            self.extracted_from.append(val)
        self.confidence = content.get("confidence", 0.0)
        self.id = content.get("id", 0)
        self.page = content.get("page", 0)
        self.headline = content.get("headline", "")
        self.subhead = content.get("subhead", "")
        self.lead = content.get("lead", "")
        self.byline = Byline(content.get("byline")) if content.get("byline") is not None else None
        self.paragraphs = []
        js_paragraph = content.get("paragraphs", [])
        for val in js_paragraph:
            self.paragraphs.append(Paragraph(val))

        

class Publication(Model):
    """
    Class structure for containing the publication content data from JSON schema: "http://json-schema.org/draft-04/schema#"
    
    Contains values:
      publication - str: The magazine or newspaper where it is published
      published_at - str: The date the publication was published
      publisher - str: The name of the publisher
      pages - int: The total number of pages
      articles - List[Articles]: A list containing the articles for the publication
    """
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
        js_article = content.get("articles", [])
        for val in js_article:
            self.articles.append(Article(val))
