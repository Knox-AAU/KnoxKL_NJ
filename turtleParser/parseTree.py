from turtleParser.node import Node
from turtleParser.categories import Categories

class ParseTree:
    def __init__(self, text):
        """
        The parse tree

        Input:
            text: str - a turtle(ttl.) string to be parsed
        """
        self.root = Node(Categories.turtleDoc, 0)
        self.text = text

    def match(self, char, node):
        """
        Matches a single char.

        Input:
            char: str - a single char, digit and symbol.
            node: Node - a node with an index pointing a char in the parsing string that has to be matched.
        
        Return:
            bool - True = successful match. False = unsuccessful match.
        """

        #If index outside parsing string bounds
        if node.Index() >= len(self.text):
            return False

        #If match found
        if self.text[node.StartIndex+node.Size] == str(char):
            #Then add node
            node.addLiteral(char)
            return True

        #Else no match found
        return False

    def matchUntil(self, char, node):
        """
        Adds all chars from the parsing string until it ends with a specified char.

        Input:
            char: str - A single char, digit or symbol that the sequence have to end with.
            node: The node all the literals have to be added to.
        Return:
            bool - True = successful match. False = unsuccessful match.
        """
        while True:
            #If index outside parsing string bounds
            if node.Index() >= len(self.text):
                return False
 
            #If the index of the parsing char matches the specified char
            if self.text[node.Index()] == str(char):
                #Then it must be the last char to be added
                node.addLiteral(self.text[node.Index()])
                return True

            #Add whatever char and continue
            node.addLiteral(self.text[node.Index()])

    def skip(self, char, node):
        """
        Skips chars in parsing string that matches specified char

        Input:
            char: str - The char used to match the char of the parsing string
            node: Node - Node containing an index for the parsing string
        
        Return:
            bool - True = successful skip. False = no skip.
        """
        if self.match(char, node):
            return True
        return False
        
    def matchString(self, string, node):
        """
        Matches a whole string

        Input:
            string: str - The string used for matching a part of the parsing string
            node: Node - Node containing a index for the parsing string
        
        Return:
            bool - True = successful match. False = unsuccessful match.
        """
        for char in string:
            if not self.match(char, node):
                return False
        return True

    def matchList(self, stringList, node):
        '''
        Matches a single char with multiple possible chars

        Input:
            stringList: str - A list containing all chars that can be matched with
            node: Node - Node containing a index for the parsing string
        
        Return:
            bool - True = successful match. False = unsuccessful match.
        '''
        for char in stringList:
            if (self.match(char, node)):
                return True
        return False

    def getLastChar(self, node):
        '''
        Get the last char of a node based on the index of the node

        Input:
            node: Node - Node containing a index for the parsing string
        
        Return:
            char: str - The last char that a node covers
        '''
        char = self.text[node.Index()-1]
        return char

    def printTree(self):
        '''
        Prints the tree of the parsing tree starting from the root
        '''
        self.root.printChildren()