from rdflib.namespace import ClosedNamespace
from environment.EnvironmentConstants import EnvironmentVariables as ev
from turtleParser.turtleParser import RuntimeOntology as ro
from rdflib import URIRef

KNOX = ClosedNamespace(
    uri=URIRef(ro.instance.GetOntologyNamespace()),
    terms=[
        "isPublishedBy", "mentions", "isPublishedOn", "publishes", "Email", "DateMention", "Link",
        "Name", "PublicationDay", "PublicationMonth", "PublicationYear", "ArticleTitle", "isWrittenBy"]
)