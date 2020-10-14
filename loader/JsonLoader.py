from __future__ import annotations
import json
import datetime
from typing import List
from itertools import groupby
from operator import itemgetter


def load_json(json_path: str) -> NewsStruct:
    """
    Input:
        json_path: str - The path to the json news struct
    
    Returns:
        A news struct
    
    This function creates and loads a news struct into memort
    """
    return NewsStruct(json_path)


class NewsStruct:
    """
    This structure contains information about about an edition of a news paper.
    This information will be loaded from a given file, provided by the previous layer.
    """
    publications: List[Publication] = []
    articles: List[Article] = []
    __json__: List[dict] = []
    __raw_articles__: dict = {}

    def __init__(self, json_path: str) -> NewsStruct:
        """
        Input:
            jsonPath

        Loads the json file into the class as a dictionary, on the property json.
        """
        with open(json_path, "r", encoding="utf-8") as json_file:
            self.__json__ = json.load(json_file)

        self.__json__ = sorted(self.__json__, key=lambda item: (
            item['content']['publication'], item['content']['page'], item['content']['publishedAt'], item['content']['publisher'], item['content']['nmId'], item['content']['byline']['name']))
        

    def load_publications(self) -> None:
        """
        Loads all publications into a two dimensional array.
        This two dimensional array will later be used to create publication objects for a given newspaper

        """

        publication_name = ""
        for index in range(len(self.__json__)):
            indexed_publication_name = self.__json__[
                index]['content']['publication'].replace(' ', '_')

            # If the name is not the same, we have a new publication
            if publication_name != indexed_publication_name:
                self.__raw_articles__[indexed_publication_name] = []
                publication_name = indexed_publication_name

            # We do not wish to clutter our articles with empty or none-existing paragraphs
            if 'paragraphs' not in self.__json__[index]['content'].keys() or len(self.__json__[index]['content']['paragraphs']) == 0:
                continue

            self.__raw_articles__[indexed_publication_name].append(self.__json__[
                                                                   index])

        for key in self.__raw_articles__.keys():
            self.publications.append(Publication(
                key, self.__raw_articles__[key]))

        for publication in self.publications:
            for article in publication.articles:
                self.articles.append(article)

    def __repr__(self):
        """
        Returns:
            A string representation of object

        Equivalent of toString()
        """
        return str({
            "publications": str(self.publications),
            "articles": str(self.articles)
        })


class Publication:
    """
    This struct contains a collection of articles, from a given publisher.
    This information is created based on information gathered in a NewsStruct
    """

    def __init__(self, publisher: str, article_dicts: list) -> Publication:
        """
        Input:
            publisher: str - The name of the publisher
            publicatioDicts: list - A list of all publications

        Constructor for the publication object
        """
        self.publisher = publisher
        self.__article_dicts__ = article_dicts
        self.articles = []
        for article_dict in self.__article_dicts__:
            self.articles.append(Article(article_dict))

    def __repr__(self):
        """
        Returns:
            A string representation of object

        Equivalent of toString()
        """
        return str({"publisher": self.publisher, "articles": self.articles})


class Article:
    """
    This structure contains information about a single article, its publisher, the paragraphs.
    The Article will be created based on information from the NewsStruct object.
    """

    def __init__(self, article_dict: dict) -> Article:
        """
        Input:
            article_dict: dict - A dictionary containing information about a given article

        Constructor for the article object
        """
        self.title = article_dict['content']['title']
        self.publishedAt = article_dict['content']['publishedAt']
        self.nmId = article_dict['content']['nmId']
        self.authorName = article_dict['content']['byline']['name']
        self.content = ' '.join(
            [value['value'] for value in article_dict['content']['paragraphs']])

    def __repr__(self):
        """
        Returns:
            A string representation of object

        Equivalent of toString()
        """
        return str({"title": self.title, "content": self.content})
