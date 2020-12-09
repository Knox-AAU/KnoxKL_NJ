from enum import Enum

class Categories(Enum):
    '''
    Node categories used for specifing the terminal/nonterminal production used for every node.
    '''
    turtleDoc = 1
    statement = 2
    directive = 3
    prefixID = 5
    PNAME_LN = "pname_ln"
    subject = "subject"
    triples = "triples"
    verb = "verb"
    obj = "object"
    PNAME_NS = 139
    IRIREF = 18
    PN_CHARS_BASE = 1163
    PN_CHARS_U = 1164
    PN_CHARS = 1166
    prefix = 1000
    PN_PREFIX = "167s"
    PN_PREFIXONE = 10001
    PN_PREFIXONEONE = 10002
    PN_LOCALTwoTwo = 144
    PN_LOCALTwoOne = 1455
    PN_LOCALOne = 1680
    PN_LOCALTwo = 1681
    literal = 100000
    initial = 100001
    test = 100002
    haha = 2222222