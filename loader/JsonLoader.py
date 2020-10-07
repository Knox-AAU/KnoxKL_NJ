import json
import datetime
from itertools import groupby
from operator import itemgetter


class NewsStruct:
    """
    This structure contains information about about an edition of a news paper.
    This information will be loaded from a given file, provided by the previous layer.
    """
    publications = []
    
    def __init__(self, json_path:str):
        """
        Input:
            jsonPath
        
        Loads the json file into the class as a dictionary, on the property json.
        """
        with open(json_path, "r") as json_file:
            self.__json__ = json.load(json_file)
        
        self.__json__ = sorted(self.__json__, key=lambda item: (item['content']['publication'], item['content']['page']))
    
    def load_publications(self) -> list:
        """
        Loads all publications into a two dimensional array.
        This two dimensional array will later be used to create publication objects for a given newspaper

        """
        self.__raw_articles__: dict = {}
        publication_name = ""
        for index in range(len(self.__json__)):
            indexed_publication_name = self.__json__[index]['content']['publication'].replace(' ', '_')

            # If the name is not the same, we have a new publication
            if publication_name != indexed_publication_name:
                self.__raw_articles__[indexed_publication_name] = []
                publication_name = indexed_publication_name
            
            # We do not wish to clutter our articles with empty or none-existing paragraphs
            if 'paragraphs' not in self.__json__[index]['content'].keys() or len(self.__json__[index]['content']['paragraphs']) == 0:
                continue

            self.__raw_articles__[indexed_publication_name].append(self.__json__[index])
        
        for key in self.__raw_articles__.keys():
            self.publications.append(Publication(key,self.__raw_articles__[key]))

class Publication:
    """
    This struct contains a collection of articles, from a given publisher.
    This information is created based on information gathered in a NewsStruct
    """
    def __init__(self, publisher:str, publication_dicts:list):
        """
        Input:
            publisher: str - The name of the publisher
            publicatioDicts: list - A list of all publications

        Constructor for the publication object
        """
        self.publisher = publisher
        self.__pub_dict__ = publication_dicts

class Article:
    """
    This structure contains information about a single article, its publisher, the paragraphs.
    The Article will be created based on information from the NewsStruct object.
    """

    def __init__(self, article_dicts:list):
        """"""
