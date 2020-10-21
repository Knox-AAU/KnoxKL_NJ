from rdflib.namespace import ClosedNamespace
from environment.EnvironmentConstants import EnvironmentVariables as ev
from rdflib import URIRef

KNOX = ClosedNamespace(
    uri=URIRef(ev().get_value(ev().KNOX_18_NAMESPACE, "http://www.thisistesturl.example/")),
    terms=[
        "isPublishedBy", "mentions", "isPublishedOn", "publishes", "Email", "DateMention", "Link",
        "Name", "PublicationDate", "ArticleTitle", "isWrittenBy"]
)
