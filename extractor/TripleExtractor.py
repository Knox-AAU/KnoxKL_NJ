from __future__ import annotations
from typing import List, OrderedDict
from turtleParser.turtleParser import RuntimeOntology as ro
from knox_source_data_io.models.publication import Publication, Article
from rdf.RdfConstants import RelationTypeConstants
from rdf.RdfCreator import generate_uri_reference, generate_relation, generate_literal, store_rdf_triples
from extractor.TripleExtractorEnum import TripleExtractorEnum
from preproc import PreProcessor
from knox_util import print, convert_iso_string_to_date_time
from extractor.WordFrequencyHandler import WordFrequencyHandler


class TripleExtractor:

    nlp: OrderedDict = None
    def __init__(self, tuple_label_list=None, ignore_label_list=None) -> None:
        PreProcessor.nlp = self.nlp
        self.namespace = ro.instance.GetOntologyNamespace()
        self.triples = []
        self.named_individual = []
        self.preprocess_year_threshold = 1948
        if tuple_label_list is None:
            self.tuple_label_list = [["PER", "Person"], ["ORG", "Organisation"], ["LOC", "Location"], ["DATE", "Date"], ["MEDICAL", "Medical"]]
        else:
            self.tuple_label_list = tuple_label_list
        if ignore_label_list is None:
            self.ignore_label_list = ["MISC"]
        else:
            self.ignore_label_list = ignore_label_list
        
        self.word_frequency_handler = WordFrequencyHandler()

    def add_named_individual(self, prop_1, prop_2) -> None:
        """
        Adds the named individuals to the named_individual list if it's not already in it.
        """
        if [prop_1, prop_2] not in self.named_individual:
            self.named_individual.append([prop_1, prop_2])

    def extract_publication(self, pub: Publication) -> None:
        # Name of a publications publisher
        name = pub.publisher.replace(" ", "_")

        # Name of the publication
        pub_name = pub.publication.replace(" ", "_")

        # Adds publication as a named individual
        self.add_named_individual(pub_name, TripleExtractorEnum.PUBLICATION)

        # Add publisher name as data property
        self.triples.append([
            generate_uri_reference(self.namespace, [TripleExtractorEnum.PUBLISHER], name),
            generate_relation(RelationTypeConstants.KNOX_NAME),
            generate_literal(name)])

        # Add the "Publisher publishes Publication" relation
        self.triples.append([
            generate_uri_reference(self.namespace, [TripleExtractorEnum.PUBLISHER], name),
            generate_relation(RelationTypeConstants.KNOX_PUBLISHES),
            generate_uri_reference(self.namespace, [TripleExtractorEnum.PUBLICATION], pub_name)
        ])
        # Add publication name as data property
        self.triples.append([
            generate_uri_reference(self.namespace, [TripleExtractorEnum.PUBLICATION], pub_name),
            generate_relation(RelationTypeConstants.KNOX_NAME),
            generate_literal(pub.publication)
        ])

    def convert_spacy_label_to_namespace(self, string: str) -> str:
        """
        Input:
            string: str - A string matching a spacy label
        Returns:
            A string matching a class in the ontology.
        """
        for label_tuple in self.tuple_label_list:
            # Assumes that tuple_label_list is a list of tuples with the format: [spacy label, namespace]
            if string == str(label_tuple[0]):
                # return the chosen name for the spaCy label
                return str(label_tuple[1])
        else:
            return string

    def process_article_text(self, article_text: str) -> List[(str, str)]:
        """
        Input:
            article_text: str - The entire content of an article
        Returns:
            A list of "string" and label pairs. Eg: [("Jens Jensen", Person), ...]

        Runs the article text through the spacy pipeline
        """
        # Do nlp
        doc = self.nlp(article_text)

        # Create article entity from the document entities
        article_entities = []

        for entities in doc.ents:
            name = entities.text
            # label_ is correct for acquiring the spaCy string version of the entity
            label = entities.label_

            # ignore ignored labels, expects ignore_label_list to be a list of strings
            if label not in self.ignore_label_list:
                # Add entity to list, create it as named individual.
                article_entities.append((name, label))
                self.add_named_individual(name.replace(" ", "_"), self.convert_spacy_label_to_namespace(label))
        return article_entities

    def process_article(self, article: Article, doPreprocessing: bool = False) -> None:
        """
        Input:
            article: Article - An Article object from the loader package
            doPreprocessing: bool - A boolean determining if preprocessing should be done on the content before entity extraction (default: False)
        Returns:
            A list of triples with subjects, predicates and objects from the article eg.
            ("Article", "mentions", "Folketinget")
        """

        # Article text is split into multiple paragraph objects in the Json, this is joined into one string.
        content = ' '.join(para.value for para in article.paragraphs).replace('”', '"')

        # Count the word frequency
        self.word_frequency_handler.do_word_count_for_article(article.headline, content, article.extracted_from)

        # Run preprocessing steps on the content if "doPreprocessing" is True
        if doPreprocessing:
            print('Running preprocessing for content of article with ID: <' + str(article.id) + '>')
            content = PreProcessor.remove_stop_words(content)
            content = PreProcessor.convert_to_modern_danish(content)

        # Does nlp on the text
        article_entities = self.process_article_text(content)

        for pair in article_entities:
            # Ensure formatting of the objects name is compatible, eg. Jens Jensen -> Jens_Jensen
            object_ref = str(pair[0]).replace(" ", "_")

            # Changes spacy labels to full length labels
            object_label = str(pair[1])
            object_label = self.convert_spacy_label_to_namespace(object_label)

            # Each entity in article added to the "Article mentions Entity" triples
            _object = generate_uri_reference(self.namespace, [object_label], object_ref)
            _subject = generate_uri_reference(self.namespace, [TripleExtractorEnum.ARTICLE], str(article.id))
            relation = generate_relation(RelationTypeConstants.KNOX_MENTIONS)

            self.triples.append([_subject, relation, _object])
            # Each entity given the name data property
            self.triples.append(
                [_object, generate_relation(RelationTypeConstants.KNOX_NAME), generate_literal(pair[0])])

    def extract_article(self, article: Article, publication: Publication) -> None:
        """
        Input:
            article: Article - An instance of the article from input file
            publication: Publication - The publication object holding information about a publicaion

        Creates triple based on data received through the input file
        """
        # id of the article
        article_id = str(article.id)

        # Creates the article as a named individual
        self.add_named_individual(article_id, TripleExtractorEnum.ARTICLE)
        # Creates the publisher as a named individual
        self.add_named_individual(publication.publisher.replace(" ", "_"), TripleExtractorEnum.PUBLISHER)

        # Adds the Article isPublishedBy Publication relation to the turtle output
        self.triples.append([
            generate_uri_reference(self.namespace, [TripleExtractorEnum.ARTICLE], article_id),
            generate_relation(RelationTypeConstants.KNOX_IS_PUBLISHED_BY),
            generate_uri_reference(self.namespace, [TripleExtractorEnum.PUBLISHER],
                                   publication.publisher.replace(" ", "_"))
        ])

        # Adds the Article knox:Article_Title Title data to the turtle output
        self.triples.append([
            generate_uri_reference(self.namespace, [TripleExtractorEnum.ARTICLE], article_id),
            generate_relation(RelationTypeConstants.KNOX_ARTICLE_TITLE),
            generate_literal(article.headline)
        ])

        # If the byline exists add the author name to the RDF triples. Author name is required if byline exists.
        if article.byline is not None:
            # article.byline.name stores the author of the article's name, hence author_name
            author_name = article.byline.name.replace(" ", "_")

            self.triples.append([
                generate_uri_reference(self.namespace, [TripleExtractorEnum.AUTHOR], author_name),
                generate_relation(RelationTypeConstants.KNOX_NAME),
                generate_literal(article.byline.name)
            ])

            # Creates the author as a named individual
            self.add_named_individual(author_name, TripleExtractorEnum.AUTHOR)
            # Adds the Article isWrittenBy Author relation to the triples list
            self.triples.append([
                generate_uri_reference(self.namespace, [TripleExtractorEnum.ARTICLE], article_id),
                generate_relation(RelationTypeConstants.KNOX_IS_WRITTEN_BY),
                generate_uri_reference(self.namespace, [TripleExtractorEnum.AUTHOR], author_name)
            ])

            # Since email is not required in the byline, if it exists: add the authors email as a data property to the author.
            if article.byline.email is not None:
                self.triples.append([
                    generate_uri_reference(self.namespace, [TripleExtractorEnum.AUTHOR], author_name),
                    generate_relation(RelationTypeConstants.KNOX_EMAIL),
                    generate_literal(article.byline.email)
                ])

        # Adds the publication date to the article, if it exists.
        if publication.published_at != "":
            datetime = convert_iso_string_to_date_time(publication.published_at)
            self.triples.append([
                generate_uri_reference(self.namespace, [TripleExtractorEnum.ARTICLE], article_id),
                generate_relation(RelationTypeConstants.KNOX_PUBLICATION_DAY),
                generate_literal(datetime.day)
            ])
            self.triples.append([
                generate_uri_reference(self.namespace, [TripleExtractorEnum.ARTICLE], article_id),
                generate_relation(RelationTypeConstants.KNOX_PUBLICATION_MONTH),
                generate_literal(datetime.month)
            ])
            self.triples.append([
                generate_uri_reference(self.namespace, [TripleExtractorEnum.ARTICLE], article_id),
                generate_relation(RelationTypeConstants.KNOX_PUBLICATION_YEAR),
                generate_literal(datetime.year)
            ])

        # For each file that an article is extracted from, add it to the article as a data property
        if len(article.extracted_from) > 0:
            for ocr_file in article.extracted_from:
                self.triples.append([
                    generate_uri_reference(self.namespace, [TripleExtractorEnum.ARTICLE], article_id),
                    generate_relation(RelationTypeConstants.KNOX_LINK),
                    generate_literal(ocr_file)
                ])

    def append_named_individual(self) -> None:
        """
        Appends each named individual to the triples list.
        """

        # prop1 = The specific location/person/organisation or so on
        # prop2 = The type of Knox:Class prop1 is a member of.
        for prop1, prop2 in self.named_individual:
            self.triples.append([
                generate_uri_reference(self.namespace, [prop2], prop1),
                generate_relation(RelationTypeConstants.RDF_TYPE),
                generate_relation(RelationTypeConstants.OWL_NAMED_INDIVIDUAL)
            ])

            self.triples.append([
                generate_uri_reference(self.namespace, [prop2], prop1),
                generate_relation(RelationTypeConstants.RDF_TYPE),
                generate_uri_reference(self.namespace, ref=prop2)
            ])

    def process_publication(self, publication: Publication, file_path: str) -> None:
        """
        Input:
            publication: Publication - A Publication class which is the content of a newspaper
            file_path : str - File path to the publication being processed

        Writes entity triples to file
        """
        # Extract publication info and adds it to the RDF triples.
        self.extract_publication(publication)

        # Do check for preprocessing threshold
        datetime = convert_iso_string_to_date_time(publication.published_at)
        preprocess = datetime.year < self.preprocess_year_threshold

        for article in publication.articles:
            # For each article, process the text and extract non-textual data in it.
            self.process_article(article, preprocess)
            self.extract_article(article, publication)

        # Adds named individuals to the triples list.
        self.append_named_individual()

        # Function from rdf.RdfCreator, writes triples to file
        store_rdf_triples(self.triples, file_path)

        self.word_frequency_handler.send_pending_counts(file_path)
