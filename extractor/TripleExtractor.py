from __future__ import annotations
import spacy
from environment.EnvironmentConstants import EnvironmentVariables as ev
from loader.JsonWrapper import Publication, Article
from rdf.RdfConstants import RelationTypeConstants
from rdf.RdfCreator import generate_uri_reference, generate_relation, generate_literal, store_rdf_triples


class TripleExtractor:

    def __init__(self, model, tuple_label_list=None, ignore_label_list=None):
        self.nlp = spacy.load(model)
        # TODO remove hardcoded namespace
        self.namespace = ev().get_value(ev().KNOX_18_NAMESPACE, "http://www.thisistesturl.example/")
        self.triples = []
        self.named_individual = []
        if tuple_label_list is None:
            self.tuple_label_list = [["PER", "Person"], ["ORG", "Organisation"], ["LOC", "Location"]]
        else:
            self.tuple_label_list = tuple_label_list
        if ignore_label_list is None:
            self.ignore_label_list = ["MISC"]
        else:
            self.ignore_label_list = ignore_label_list

    def add_named_individual(self, prop_1, prop_2):
        """
        Adds the named individuals to the named_individual list if it's not already in it.
        """
        if [prop_1, prop_2] not in self.named_individual:
            self.named_individual.append([prop_1, prop_2])

    def extract_publication(self, pub: Publication):
        # Name of a publications publisher
        name = pub.publisher.replace(" ", "_")

        # Name of the publication
        pub_name = pub.publication.replace(" ", "_")

        # Adds publication as a named individual
        self.add_named_individual(pub.publication.replace(" ", "_"), "Publication")

        # Add publisher name as data property
        self.triples.append([
            generate_uri_reference(self.namespace, ["Publisher"], name),
            generate_relation(RelationTypeConstants.KNOX_NAME),
            generate_literal(name)])

        # Add the "Publisher publishes Publication" relation
        self.triples.append([
            generate_uri_reference(self.namespace, ["Publisher"], name),
            generate_relation(RelationTypeConstants.KNOX_PUBLISHES),
            generate_uri_reference(self.namespace, ["Publication"], pub_name)
        ])
        # Add publication name as data property
        self.triples.append([
            generate_uri_reference(self.namespace, ["Publication"], pub_name),
            generate_relation(RelationTypeConstants.KNOX_NAME),
            generate_literal(pub.publication)
        ])

    def convert_spacy_label_to_namespace(self, string: str):
        """
        Input:
            A string matching a spacy label
        Returns:
            A string matching a class in the ontology.
        """
        for label_tuple in self.tuple_label_list:
            # Assumes that tuple_label_list is a list of tuples with the format: [spacy label, namespace]
            if string == str(label_tuple[0]):
                return str(label_tuple[1])
        else:
            return string

    def process_article_text(self, article_text: str):
        """
        Input:
            Takes a string
        Returns:
            A list of "string" and label pairs. Eg: [("Jens Jensen", Person), ...]

        Runs the article text through the spacy pipeline
        """
        # Do nlp
        doc = self.nlp(article_text)

        # Create article entity from the document entitites
        article_entities = []

        for entities in doc.ents:
            name = entities.text
            # label_ is correct for acquiring the spaCy string version of the entity
            label = entities.label_

            # Add entity to list, create it as named individual.
            article_entities.append((name, label))
            self.add_named_individual(name.replace(" ", "_"), self.convert_spacy_label_to_namespace(label))

        return article_entities

    def process_article(self, article: Article):
        """
        Input:
            An Article object from the loader package
        Returns:
            A list of triples with subjects, predicates and objects from the article eg.
            ("Article", "mentions", "Folketinget")
        """

        # Article text is split into multiple paragraph objects in the Json, this is joined into one string.
        content = ' '.join(para.value for para in article.paragraphs)

        # Does nlp on the text
        article_entities = self.process_article_text(content)

        for pair in article_entities:
            # Ensure formatting of the objects name is compatible, eg. Jens Jensen -> Jens_Jensen
            object_ref = str(pair[0]).replace(" ", "_")

            # Changes spacy labels to full length labels
            object_label = str(pair[1])
            object_label = self.convert_spacy_label_to_namespace(object_label)

            # Ignore ignored labels
            for label in self.ignore_label_list:
                if object_label == str(label[0]):
                    continue

            # Each entity in article added to the "Article mentions Entity" triples
            _object = generate_uri_reference(self.namespace, [object_label], object_ref)
            _subject = generate_uri_reference(self.namespace, ["Article"], str(article.id))
            relation = generate_relation(RelationTypeConstants.KNOX_MENTIONS)

            self.triples.append([_subject, relation, _object])
            # Each entity given the name data property
            self.triples.append(
                [_object, generate_relation(RelationTypeConstants.KNOX_NAME), generate_literal(pair[0])])
        return

    def extract_article(self, article: Article, publication: Publication):
        """
        Input:
            Takes an Article and Publication object from the loader.JsonWrapper package.

            Creates the RDF triples unique to the article.
        """

        # Creates the article as a named individual
        self.add_named_individual(str(article.id), "Article")
        # Creates the publisher as a named individual
        self.add_named_individual(publication.publisher.replace(" ", "_"), "Publisher")

        # Adds the Article isPublishedBy Publication relation to the turtle output
        self.triples.append([
            generate_uri_reference(self.namespace, ["Article"], str(article.id)),
            generate_relation(RelationTypeConstants.KNOX_IS_PUBLISHED_BY),
            generate_uri_reference(self.namespace, ["Publisher"], publication.publisher.replace(" ", "_"))
        ])

        # Adds the Article knox:Article_Title Title data to the turtle output
        self.triples.append([
            generate_uri_reference(self.namespace, ["Article"], str(article.id)),
            generate_relation(RelationTypeConstants.KNOX_ARTICLE_TITLE),
            generate_literal(article.headline)
        ])

        # If the byline exists add the author name to the RDF triples. Author name is required if byline exists.
        if article.byline is not None:
            self.triples.append([
                generate_uri_reference(self.namespace, ["Author"], article.byline.name.replace(" ", "_")),
                generate_relation(RelationTypeConstants.KNOX_NAME),
                generate_literal(article.byline.name)
            ])
            # Creates the author as a named individual
            self.add_named_individual(article.byline.name.replace(" ", "_"), "Author")
            # Adds the Article isWrittenBy Author relation to the triples list
            self.triples.append([
                generate_uri_reference(self.namespace, ["Article"], str(article.id)),
                generate_relation(RelationTypeConstants.KNOX_IS_WRITTEN_BY),
                generate_uri_reference(self.namespace, ["Author"], article.byline.name.replace(" ", "_"))
            ])
            # Since email is not required in the byline, if it exsists: add the authors email as a data property to the author.
            if article.byline.email is not None:
                self.triples.append([
                    generate_uri_reference(self.namespace, ["Author"], article.byline.name.replace(" ", "_")),
                    generate_relation(RelationTypeConstants.KNOX_EMAIL),
                    generate_literal(article.byline.email)
                ])

        # Adds the publication date to the article, if it exists.
        if publication.published_at != "":
            self.triples.append([
                generate_uri_reference(self.namespace, ["Article"], str(article.id)),
                generate_relation(RelationTypeConstants.KNOX_PUBLICATION_DATE),
                generate_literal(publication.published_at)
            ])

        # For each file that an article is extracted from, add it to the article as a data property
        if len(article.extracted_from) > 0:
            for ocr_file in article.extracted_from:
                self.triples.append([
                    generate_uri_reference(self.namespace, ["Article"], str(article.id)),
                    generate_relation(RelationTypeConstants.KNOX_LINK),
                    generate_literal(ocr_file)
                ])
        return

    def write_named_individual(self):
        """
        Writes each named individual to the file.
        """

    
        #prop1 = The specific location/person/organisation or so on
        #prop2 = The type of Knox:Class prop1 is a member of.
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


    def process_publication(self, publication: Publication):
        """
        Input:
            A NewsStruct from the loader package.


        Writes entity triples to file
        """
        # Extract publication info and adds it to the RDF triples.
        self.extract_publication(publication)
        for article in publication.articles:
            # For each article, process the text and extract non-textual data in it.
            self.process_article(article)
            self.extract_article(article, publication)

        # Writes named individuals to the output file.
        self.write_named_individual()


        # Function from rdf.RdfCreator, writes triples to file
        store_rdf_triples(self.triples)

		