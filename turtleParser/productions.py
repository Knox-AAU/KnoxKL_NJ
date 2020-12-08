#The productions of this parser follows the official turtle(.ttl) grammar: https://www.w3.org/TR/turtle/#grammar-production-PNAME_NS
import turtleParser.util as util
from turtleParser.categories import Categories
from turtleParser.node import Node
from turtleParser.parseTree import ParseTree

#NONTERMINALS
#1 (statements)*
#Modified for comments
def TurtleDoc(pt):
    new = Node(Categories.turtleDoc, 0)

    #Comment | prefixID
    while True:
        while(pt.skip('\n', new) or pt.skip(' ', new) or pt.skip('\t', new)):
            pass
        #Comment
        if pt.match('#', new):
            if pt.matchUntil("\n", new):
                continue
            pt.root = new
            return 
        #Statement
        temp = Statement(pt, new)
        if temp.Size > 0:
            new.add(temp)
            continue
        pt.root = new
        return 

def Statement(pt, parent):
    new = Node(Categories.statement, parent.Index())

    #directive
    temp = Directive(pt, new)
    if temp.Size > 0:
        new.add(temp)
        return new

    #triples
    temp = triples(pt, new)
    if temp.Size > 0:
        new.add(temp)
        return new

    
    return new

#3 prefixID | base | sparqlPrefix | sparqlBase
def Directive(pt, parent):
    new = Node(Categories.directive, parent.Index())

    #prefixID
    temp = PrefixID(pt, new)
    if temp.Size > 0:
        new.add(temp)
        return new

    return new

#4 prefixID '@prefix' PNAME_NS IRIREF '.'
# There have to be space before '.'
def PrefixID(pt, parent):
    new = Node(Categories.prefixID, parent.Index())

    #'@prefix'
    if not pt.matchString("@prefix", new):
        return new

    # ' '
    if not pt.skip(' ', new):
        new.trash()
        return new 
    while(pt.skip(' ', new)):
        pass
    #PNAME_NS
    temp = PNAME_NS(pt, new)
    if temp.Size == 0:
        new.trash()
        return new
    new.add(temp)

    # ' '
    if not pt.skip(' ', new):
        new.trash()
        return new 
    while(pt.skip(' ', new)):
        pass

    #IRIREF
    temp = IRIREF(pt, new)
    if temp.Size == 0:
        new.trash()
        return new
    new.add(temp)

    # ' '
    if not pt.skip(' ', new):
        new.trash()
        return new 
    while(pt.skip(' ', new)):
        pass
    #'.'
    if not pt.match('.', new):
        new.trash()
        return new

    return new

#6 subject predicateObjectList 
def triples(pt, parent):
    new = Node(Categories.triples, parent.Index())

    #subject
    temp = subject(pt, new)
    if temp.Size == 0:
        return new
    new.add(temp)

    #(' ' | '\n' | '\t')
    while(pt.skip('\n', new) or pt.skip(' ', new) or pt.skip('\t', new)):
        pass

    #predicateObjectList
    temp = predicateObjectList(pt, new)
    if temp.Size == 0:
        new.trash()
        return new
    new.add(temp)

    #' '
    pt.skip('.', new)
    return new

#7 verb objectList
def predicateObjectListOneOne(pt, parent):
    new = Node(Categories.turtleDoc, parent.Index())

    #verb
    temp = verb(pt, new)
    if temp.Size == 0:
        return new
    new.add(temp)

    #' '
    pt.skip(' ', new)
    
    #objectList
    temp = objectList(pt, new)
    if temp.Size == 0:
        new.trash()
        return new
    new.add(temp)
    return new

#7  ';' (verb objectList)?
def predicateObjectListOne(pt, parent):
    new = Node(Categories.turtleDoc, parent.Index())

    if not pt.match(';', new):
        return new

    #(' ' | '\n' | '\t')
    while(pt.skip('\n', new) or pt.skip(' ', new) or pt.skip('\t', new)):
        pass

    temp = predicateObjectListOneOne(pt, new)
    if temp.Size > 0:
        new.add(temp)
        return new

    return new

#7  verb objectList (';' (verb objectList)?)*
def predicateObjectList(pt, parent):
    new = Node(Categories.turtleDoc, parent.Index())

    #verb
    temp = verb(pt, new)
    if temp.Size == 0:
        return new
    new.add(temp)

    #(' ' | '\n' | '\t')
    while(pt.skip('\n', new) or pt.skip(' ', new) or pt.skip('\t', new)):
        pass

    #objectList
    temp = objectList(pt, new)
    if temp.Size == 0:
        new.trash()
        return new
    new.add(temp)

    #(' ' | '\n' | '\t')
    while(pt.skip('\n', new) or pt.skip(' ', new) or pt.skip('\t', new)):
        pass
    
    #(';' (verb objectList)?)*
    while True:
        #' '
        pt.skip(' ', new)       
        temp = predicateObjectListOne(pt, new)
        if temp.Size > 0:
            new.add(temp)
            continue
        break
    return new

#8  ',' obj
def objectListOne(pt, parent):
    new = Node(Categories.turtleDoc, parent.Index())

    if not pt.match(',', new):
        return new
    
    #(' ' | '\n' | '\t')
    while(pt.skip('\n', new) or pt.skip(' ', new) or pt.skip('\t', new)):
        pass

    #obj
    temp = obj(pt, new)
    if temp.Size > 0:
        new.add(temp)
        return new

    new.trash()
    return new

#8 object (',' object)*
def objectList(pt, parent):
    new = Node(Categories.turtleDoc, parent.Index())
    
    #object
    temp = obj(pt, new)
    if temp.Size == 0:
        return new
    new.add(temp)


    #(',' object)*
    while True:
        #' '
        pt.skip(' ', new)       
        temp = objectListOne(pt, new)
        if temp.Size > 0:
            new.add(temp)
            continue
        break
    return new

#9 predicate | 'a'
def verb(pt, parent):
    new = Node(Categories.verb, parent.Index())

    #predicate
    temp = iri(pt, parent)

    if temp.Size > 0:
        new.add(temp)
        return new

    if pt.match('a', new):
        return new
    
    return new

#10 iri
def subject(pt, parent):
    new = Node(Categories.subject, parent.Index())
    
    #iri 
    temp = iri(pt, parent)
    if temp.Size > 0:
        new.add(temp)
        return new

    return new

#11 iri
def predicate(pt, parent):
    new = Node(Categories.turtleDoc, parent.Index())
    
    #iri 
    temp = iri(pt, parent)
    if temp.Size > 0:
        new.add(temp)
        return new

    return new

#12 obj
def obj(pt, parent):
    new = Node(Categories.obj, parent.Index())
    
    #iri 
    temp = iri(pt, parent)
    if temp.Size > 0:
        new.add(temp)
        return new

    return new

#135s IRIREF | PrefixedName
def iri(pt, parent):
    new = Node(Categories.turtleDoc, parent.Index())
    
    #IRIREF 
    temp = IRIREF(pt, parent)
    if temp.Size > 0:
        new.add(temp)
        return new
        
    #PrefixedName
    temp = PrefixedName(pt, parent)
    if temp.Size > 0:
        new.add(temp)
        return new

    return new

#136s PNAME_LN | PNAME_NS
def PrefixedName(pt, parent):
    new = Node(Categories.turtleDoc, parent.Index())
    
    #PNAME_LN 
    temp = PNAME_LN(pt, parent)
    if temp.Size > 0:
        new.add(temp)
        return new
    
    #PNAME_NS
    temp = PNAME_NS(pt, parent)
    
    if temp.Size > 0:
        new.add(temp)
        return new

    return new

#TERMINALS

#18 '<' ([^#x00-#x20<>"{}|^`\] | UCHAR)* '>'
#Changed: Catch all inside '<' and '>'. 
#Cannot use '<', '>' and space inside
def IRIREF(pt, parent):
    new = Node(Categories.IRIREF, parent.Index())
    
    # '<'
    if not pt.match('<', new):
        return new

    # ([^#x00-#x20<>"{}|^`\] | UCHAR)* '>'
    if not pt.matchUntil('>', new):
        new.trash()
        return new
    return new


#139s PN_PREFIX? ':'
def PNAME_NS(pt, parent):
    new = Node(Categories.PNAME_NS, parent.Index())

    # PN_PREFIX?
    temp = PN_PREFIX(pt, new)
    if temp.Size > 0:
        new.add(temp)

    #End with ':'
    if not pt.match(':', new):
        new.trash()
        return new
    return new

#140s PNAME_NS PN_LOCAL
def PNAME_LN(pt, parent):
    new = Node(Categories.PNAME_LN, parent.Index())
    
    # PNAME_NS
    temp = PNAME_NS(pt, new)
    if temp.Size == 0:
        return new
    new.add(temp)

    #PN_LOCAL
    temp = PN_LOCAL(pt, new)
    if temp.Size == 0:
        new.trash()
        return new

    new.add(temp)
    return new

#163s [A-Z] | [a-z]
def PN_CHARS_BASE(pt, parent): #DONE
    new = Node(Categories.PN_CHARS_BASE, parent.Index())
    pt.matchList(util.letterList(), new)
    return new

#164s PN_CHARS_BASE | '_'
def PN_CHARS_U(pt, parent): #DONE
    new = Node(Categories.PN_CHARS_U, parent.Index())
    

    #PN_CHARS_BASE
    temp = PN_CHARS_BASE(pt, new)
    if temp.Size > 0:

        new.add(temp)
        return new

    #'_'
    pt.match("_", new)
    return new

#166s PN_CHARS_U | '-' | [0-9]
def PN_CHARS(pt, parent): #DONE
    new = Node(Categories.PN_CHARS, parent.Index())

    #PN_CHARS_U
    temp = PN_CHARS_U(pt, new)

    if temp.Size > 0:
        new.add(temp)
        
        return new
    
    #'-'
    if pt.match("-", new):
        return new

    #[0-9]
    pt.matchList(util.digitList(), new)
    return new

#167saa PN_CHARS | '.'
def PN_PREFIXOneOne(pt, parent): #DONE
    new = Node(Categories.PN_PREFIXONEONE, parent.Index())

    #PN_CHARS
    temp = PN_CHARS(pt, new)
    if temp.Size > 0:
        new.add(temp)
        
        return new

    #'.'
    pt.match(".", new)
    return new

#167sa ((PN_CHARS | '.')* PN_CHARS)?
def PN_PREFIXOne(pt, parent):
    new = Node(Categories.PN_PREFIXONE, parent.Index())

    #((PN_CHARS | '.')*
    while True:
        
        #.
        if pt.match(".", new):
            continue
        
        #PN_CHARS
        temp = PN_PREFIXOneOne(pt, new)
        if temp.Size > 0:
            new.add(temp)
            continue
        break

    #End with PN_CHARS
    if len(new.Children) == 0:
        return new

    if new.Children[-1].Category != Categories.PN_PREFIXONEONE:
        new.trash()
        return new
    return new

#167s PN_CHARS_BASE ((PN_CHARS | '.')* PN_CHARS)?
def PN_PREFIX(pt, parent):
    new = Node(Categories.turtleDoc, parent.Index())

    #PN_CHARS_BASE
    temp = PN_CHARS_BASE(pt, new)
    if(temp.Size == 0):
        return new    
    new.add(temp)

    #((PN_CHARS | '.')* PN_CHARS)?
    temp = PN_PREFIXOne(pt, new)
    if(temp.Size > 0):
        new.add(temp)

    return new

#168sba (PN_CHARS | ':' | PLX)
def PN_LOCALTwoTwo(pt, parent):
    new = Node(Categories.PN_LOCALTwoTwo, parent.Index())
    
    #PN_CHARS
    temp = PN_CHARS(pt, new)
    if temp.Size > 0:
        new.add(temp)
        return new

    # ':'
    if pt.match(':', new):
        return new 

    return new

#168sba (PN_CHARS | '.' | ':' | PLX)
def PN_LOCALTwoOne(pt, parent):
    new = Node(Categories.PN_LOCALTwoOne, parent.Index())
    
    #PN_CHARS
    temp = PN_CHARS(pt, new)
    if temp.Size > 0:
        new.add(temp)
        return new

    # '.'
    if pt.match('.', new):
        return new   
    
    # ':'
    if pt.match(':', new):
        return new   
    
    return new
    
#168sb (PN_CHARS | '.' | ':' | PLX)* (PN_CHARS | ':' | PLX)
def PN_LOCALTwo(pt, parent):
    new = Node(Categories.PN_LOCALTwo, parent.Index())

    # (PN_CHARS | '.' | ':' | PLX)*
    while True:
        #PN_CHARS
        temp = PN_LOCALTwoOne(pt, new)
        if temp.Size > 0:
            new.add(temp)
            continue
        break

    # End with PN_CHARS | ':' | PLX
    
    # PN_CHARS
    if new.matchLastCategory(Categories.PN_CHARS):
        return new

    # ':'
    if new.matchLastChar(':'):
        return new

    new.trash()
    return new

#168sa PN_CHARS_U | ':' | [0-9] | PLX
def PN_LOCALOne(pt, parent):
    new = Node(Categories.PN_LOCALOne, parent.Index())
    
    #PN_CHARS_U
    temp = PN_CHARS_U(pt, new)
    if temp.Size > 0:
        new.add(temp)
        return new

    #':'
    if pt.match(':', new):
        return new

    #[0-9]
    if pt.matchList(util.digitList(), new):
        return new

    return new

#168s (PN_CHARS_U | ':' | [0-9] | PLX)
#     ((PN_CHARS | '.' | ':' | PLX)* (PN_CHARS | ':' | PLX))?
def PN_LOCAL(pt, parent):
    new = Node(Categories.PN_LOCALOne, parent.Index())

    # (PN_CHARS_U | ':' | [0-9] | PLX)
    temp = PN_LOCALOne(pt, new)
    if temp.Size == 0:
        return new

    new.add(temp) 

    #((PN_CHARS | '.' | ':' | PLX)* (PN_CHARS | ':' | PLX))?
    temp = PN_LOCALTwo(pt, new)
    if temp.Size > 0:
        new.add(temp)
        return new
    
    return new

'''
Must:
    if not pt.match("@prefix", new):
        return new

Or (a|b):
    temp = PN_CHARS(pt, new)
    if(temp.Index == 0):
        new.add(temp)
        return new

    #'.'
    pt.match("_", new)
    return new

Asterisk(*):
    while True:
        if not pt.matchList(util.letterList(), new):
            return new

Optional(?):
    pt.matchList(util.letterList(), new):
'''