import enum

class RelationTypeConstants(str, enum.Enum):
    # RDFS
    RESOURCE = "rdfs:Resource"
    CLASS = "rdfs:Class"
    LITERAL = "rdfs:Literal"
    DATATYPE = "rdfs:Datatype"
    LANGSTRING = "rdfs:langString"
    LABEL = "rdfs:label"
    RANGE = "rdfs:range"
    DOMAIN = "rdfs:domain"
    SUB_CLASS_OF = "rdfs:subClassOf"
    SUB_PROPERTY_OF = "rdfs:subPropertyOf"
    COMMENT = "rdfs:comment"
    CONTAINER = "rdfs:Container"
    CONTAINER_MEMBERSHIP_PROPERTY = "rdfs:ContainerMembershipProperty"
    MEMBER = "rdfs:member"
    SEE_ALSO = "rdfs:seeAlso"
    IS_DEFINED_BY = "rdfs:isDefinedBy"

    # RDF
    TYPE = "rdf:type"
    HTML = "rdf:HTML"
    XML_LITERAL = "rdf:XMLLiteral"
    PROPERTY = "rdf:Property"
    BAG = "rdf:Bag"
    SEQ = "rdf:Seq"
    ALT = "rdf:Alt"
    LIST = "rdf:List"
    FIRST = "rdf:first"
    REST = "rdf:rest"
    NIL = "rdf:nil"
    STATEMENT = "rdf:Statement"
    SUBJECT = "rdf:subject"
    PREDICATE = "rdf:predicate"
    OBJECT = "rdf:object"
    VALUE = "rdf:value"