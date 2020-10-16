from rdflib.namespace import ClosedNamespace
from environment.EnvironmentConstants import EnvironmentConstants as ec
from rdflib import URIRef

KNOX = ClosedNamespace(
    uri=URIRef(ec().get_value(ec().KNOX_18_NAMESPACE)),
    terms=[
        "isPublishedBy", "mentions", "isPublishedOn", "publishes", "Email", "DateMention", "Link",
        "Name", "PublicationDate", "ArticleTitle", "isWrittenBy"]
)
