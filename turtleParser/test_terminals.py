import turtleParser.productions as productions
import turtleParser.util as util
from turtleParser.categories import Categories

#18 IRIREF
def test_IRIREF_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.IRIREF(testPt, testNode)

    assert expected == actual.Size

def test_IRIREF_correctWord_letters():
    testString = "<abc>"
    expected = 5
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.IRIREF(testPt, testNode)

    assert expected == actual.Size

def test_IRIREF_correctWord_lettersSpaceLetters():
    testString = "<ab c>"
    expected = 6
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.IRIREF(testPt, testNode)

    assert expected == actual.Size

def test_IRIREF_correctWord_letters_notEOL():
    testString = "<abc> abc"
    expected = 5
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.IRIREF(testPt, testNode)

    assert expected == actual.Size

def test_IRIREF_correctWord_letters_correctStop():
    testString = "<<abc>>"
    expected = 6
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.IRIREF(testPt, testNode)

    assert expected == actual.Size

def test_IRIREF_wrongWord_letters():
    testString = "abc"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.IRIREF(testPt, testNode)

    assert expected == actual.Size

def test_IRIREF_wrongWord_wrongStart():
    testString = "abc>"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.IRIREF(testPt, testNode)

    assert expected == actual.Size

def test_IRIREF_wrongWord_wrongEnd():
    testString = "<abc"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.IRIREF(testPt, testNode)

    assert expected == actual.Size

#139s PNAME_NS
def test_PNAME_NS_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PNAME_NS(testPt, testNode)

    assert expected == actual.Size

def test_PNAME_NS_correct_semicolon():
    testString = ":"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PNAME_NS(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIX_correctWord_letters():
    testString = "abcd:"
    expected = 5
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIX_correctWord_letters_notEOL():
    testString = "abcd: abc"
    expected = 5
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIX_wrongChar_digit():
    testString = "2"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIX_wrongWord_wrongStart():
    testString = ".2"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIX_wrongWord_wrongEnd():
    testString = "abc."
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

#140s PNAME_LN
def test_PNAME_LN_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PNAME_LN(testPt, testNode)

    assert expected == actual.Size

def test_PNAME_LN_correctWord():
    testString = "myNS:class1"
    expected = 11
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PNAME_LN(testPt, testNode)

    assert expected == actual.Size

def test_PNAME_LN_correctWord():
    testString = ":class1"
    expected = 7
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PNAME_LN(testPt, testNode)

    assert expected == actual.Size

def test_PNAME_LN_correctWord_notEOL():
    testString = "myNS:class1 a class"
    expected = 11
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PNAME_LN(testPt, testNode)

    assert expected == actual.Size

def test_PNAME_LN_wrongWord():
    testString = "3332:"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PNAME_LN(testPt, testNode)

    assert expected == actual.Size

#163s PN_CHARS_BASE
def test_PN_CHARS_BASE_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS_BASE(testPt, testNode)

    assert expected == actual.Size

def test_PN_CHARS_BASE_correctChar_letter():
    testString = "a"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS_BASE(testPt, testNode)

    assert expected == actual.Size

def test_PN_CHARS_BASE_wrongChar_digit():
    testString = "2"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS_BASE(testPt, testNode)

    assert expected == actual.Size

#164s PN_CHARS_U
def test_PN_CHARS_U_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS_U(testPt, testNode)

    assert expected == actual.Size

def test_PN_CHARS_U_correctChar_letter():
    testString = "a"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS_U(testPt, testNode)

    assert expected == actual.Size

def test_PN_CHARS_U_correctChar_underscore():
    testString = "_"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS_U(testPt, testNode)

    assert expected == actual.Size

def test_PN_CHARS_U_wrongChar_digit():
    testString = "2"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS_U(testPt, testNode)

    assert expected == actual.Size

#166 PN_CHARS
def test_PN_CHARS_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS(testPt, testNode)

    assert expected == actual.Size

def test_PN_CHARS_correctChar_letter():
    testString = "a"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS(testPt, testNode)

    assert expected == actual.Size

def test_PN_CHARS_correctChar_dash():
    testString = "-"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS(testPt, testNode)

    assert expected == actual.Size

def test_PN_CHARS_correctChar_digit():
    testString = "-"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS(testPt, testNode)

    assert expected == actual.Size

def test_PN_CHARS_wrongChar_symbol():
    testString = "@"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_CHARS(testPt, testNode)

    assert expected == actual.Size

#167 PN_PREFIXOneOne
def test_PN_PREFIXOneOne_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOneOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIXOneOne_correctChar_letter():
    testString = "a"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOneOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIXOneOne_correctChar_dash():
    testString = "."
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOneOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIXOneOne_wrongChar_symbol():
    testString = "@"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOneOne(testPt, testNode)

    assert expected == actual.Size

#167 PN_PREFIXOne
def test_PN_PREFIXOne_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIXOne_correctChar_letter():
    testString = "a"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIXOne_correctWord_letters():
    testString = "abc.d"
    expected = 5
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIXOne_correctWord_letters():
    testString = "a4242-s sa"
    expected = 7
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIXOne_correctWord_letters_notEOL():
    testString = "abc.d abc"
    expected = 5
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIXOne_wrongChar_punctuation():
    testString = "."
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIXOne_wrongChar_symbol():
    testString = "@"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIXOne_wrongWord_wrongEnd():
    testString = "assa.a."
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIXOne(testPt, testNode)

    assert expected == actual.Size

#167 PN_PREFIX
def test_PN_PREFIX_none():
    testString = ""
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIX_correctChar_letter():
    testString = "a"
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIX_correctWord_letters():
    testString = "a.abc"
    expected = 5
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIX_correctWord_letters_notEOL():
    testString = "a.abc abc"
    expected = 5
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIX_wrongChar_digit():
    testString = "2"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIX_wrongWord_wrongStart():
    testString = "2abc"
    expected = 0
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

def test_PN_PREFIX_wrongWord_wrongEnd():
    testString = "abc.acb."
    expected = 1
    testPt = productions.ParseTree(testString)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_PREFIX(testPt, testNode)

    assert expected == actual.Size

#168s PN_LOCALTwoTwo
def test_PN_LOCALTwoTwo_none():
    string = ""
    expected = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwoTwo(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwoTwo_correctChar_letter():
    string = "d"
    expected = 1
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwoTwo(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwoTwo_correctChar_letter():
    string = ":"
    expected = 1
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwoTwo(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwoTwo_wrongChar_symbol():
    string = "+"
    expected = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)


    actual = productions.PN_LOCALTwoTwo(testPt, testNode)

    assert expected == actual.Size

#168s PN_LOCALTwoOne
def test_PN_LOCALTwoOne_none():
    string = ""
    expected = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwoTwo(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwoOne_correctChar_letter():
    string = "."
    expected = 1
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)


    actual = productions.PN_LOCALTwoOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwoOne_correctChar_letter():
    string = ":"
    expected = 1
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwoOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwoOne_correctChar_digit():
    string = "2"
    expected = 1
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwoOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwoOne_wrongChar_symbol():
    string = "¤"
    expected = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwoOne(testPt, testNode)

    assert expected == actual.Size

#168s PN_LOCALTWO
def test_PN_LOCALTwo_none():
    string = ""
    expected = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwoOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwo_correctChar_letter():
    string = "a"
    expected = 1
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwo(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwo_correctChar_colon():
    string = ":"
    expected = 1
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwo(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwo_correctWord_letters():
    string = "abc"
    expected = 3
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwo(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwo_correctWord_lettersColon():
    string = "ab:"
    expected = 3
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)


    actual = productions.PN_LOCALTwo(testPt, testNode)
    assert expected == actual.Size

def test_PN_LOCALTwo_correctWord_colonsLetter():
    string = "::a"
    expected = 3
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwo(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwo_wrongWord_lettersSymbol():
    string = "a#a"
    expected = 1
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwo(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwo_wrongWord_wrongStart():
    string = ";abc"
    expected = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwo(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALTwo_wrongWord_wrongEnd():
    string = "abc;"
    expected = 3
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, 0)

    actual = productions.PN_LOCALTwo(testPt, testNode)

    assert expected == actual.Size

#168s PN_LOCALOne
def test_PN_LOCALOne_CorrectChar_None():
    string = ""
    startIndex = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, startIndex)
    expected = 0

    actual = productions.PN_LOCALOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALOne_CorrectChar_letter():
    string = "f"
    startIndex = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, startIndex)
    expected = 1

    actual = productions.PN_LOCALOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALOne_CorrectChar_symbol():
    string = ":"
    startIndex = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, startIndex)
    expected = 1

    actual = productions.PN_LOCALOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALOne_CorrectChar_digit():
    string = "2"
    startIndex = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, startIndex)
    expected = 1

    actual = productions.PN_LOCALOne(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCALOne_WrongChar_symbol():
    string = "$"
    startIndex = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, startIndex)
    expected = 0

    actual = productions.PN_LOCALOne(testPt, testNode)

    assert expected == actual.Size

#168s PN_LOCAL
def test_PN_LOCAL_CorrectChar_None():
    string = ""
    startIndex = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, startIndex)
    expected = 0

    actual = productions.PN_LOCAL(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCAL_CorrectChar_letter():
    string = "f"
    startIndex = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, startIndex)
    expected = 1

    actual = productions.PN_LOCAL(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCAL_CorrectChar_symbol():
    string = ":"
    startIndex = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, startIndex)
    expected = 1

    actual = productions.PN_LOCAL(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCAL_CorrectChar_digit():
    string = "2"
    startIndex = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, startIndex)
    expected = 1

    actual = productions.PN_LOCAL(testPt, testNode)

    assert expected == actual.Size

def test_PN_LOCAL_CorrectWord_ColonsLetter():
    string = ":myCLass"
    startIndex = 0
    testPt = productions.ParseTree(string)
    testNode = productions.Node(productions.Categories.test, startIndex)
    expected = 8

    actual = productions.PN_LOCAL(testPt, testNode)

    assert expected == actual.Size