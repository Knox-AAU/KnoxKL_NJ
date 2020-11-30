from turtleParser.categories import Categories

class Node:
    def __init__(self, category, index, char=' '):
        """
        Nodes are used in the parsing tree.
        
        Input:
            Category: Categories Enum - The type/token/category of the node
            Children: Node list - All the children of the node in the parse tree
            StartIndex: The index in the text that the node starts from
            Char: Char storage only used for literal nodes.
        
        Properties:
            Size: How far the node covers from the start index. Literal nodes always covers one char equivalent to 1 in size.
        """
        self.Category = category
        self.Children = list()
        self.StartIndex = index
        self.Size = 0
        self.Char = str(char)
        
        if category == Categories.literal:
            self.Size = 1

    def Index(self):
        """
        Get the index of the next char to be parsed
        
        Returns:
            index: int - where the node starts in the string plus how many chars it covers
        """
        index = self.StartIndex + self.Size
        return index
        
    def printChildren(self):
        """
        Prints the parsingtree with categories and their size.
        """
        if len(self.Children) > 1 and self.Category != Categories.literal:
            print(self.Category.name, self.Size, '{', end = '')

        for child in self.Children:
            child.printChildren()

        if len(self.Children) > 1 and self.Category != Categories.literal:
            print('}', end = '')

    def getLiterals(self, parent):
        """
        Returns all connecting chars/literals
        """
        string = list()
        for node in parent.Children:
            string.append(self.getLiterals(node))
            if node.Category == Categories.literal:
                string.append(node.Char)
        return ''.join(string)

    def getStringsByCategory(self, category):
        """
        Get all the nodes matching the specified category
        
        Input:
            category: Categories Enum - The desired category
        """
        strings = list()
        for node in self.Children:
            if node.Category == category:
                string = self.getLiterals(node)
                if len(string) > 0:
                    strings.append(string)
            temp = node.getStringsByCategory(category)
            if len(temp) > 0:
                for string in temp:
                    strings.append(string)
        return strings

    def getNodesByCategory(self, category):
        """
        Get all the nodes matching the specified category
        
        Input:
            category: Categories Enum - The desired category
        """
        Node = list()
        for node in self.Children:
            if node.Category == category:
                Node.append(node)
            temp = node.getNodesByCategory(category)
            if len(temp) > 0:
                Node = Node + temp
        return Node
    
    def addLiteral(self, char):
        """
        Adds a literal/char node to the node.
        
        Input:
            char: str - A single char that the node will store for future extractions
        """
        self.add(Node(Categories.literal, 0, char))
    
    def matchLastCategory(self, category):
        """
        Search for category in the last branch of the node
        
        Input:
            category: Enum Categories - A specified category to search for
        
        Return:
            bool - True if category is found. False if category is not found
        """
        #If I am the correct node
        if self.Category == category:
            return True

        #If I do not have any children
        if len(self.Children) == 0:
            return False
        
        #If category is found further in branch
        if self.Children[-1].matchLastCategory(category):
            return True
        
        #Else not found
        return False

    def matchLastChar(self, char):
        """
        Match the last char at the end of the node
        
        Input:
            category: str - A specified char to search for
        
        Return:
            bool - True if last char matches specfied char. False if last char do not match.
        """
        #If this node is the endning node
        if len(self.Children) == 0:
            #If the endning node have the correct char
            if self.Char == char:
                return True
            return False
        
        #Else search further in the last branch
        if self.Children[-1].matchLastChar(char):
            return True
        return False


    def add(self, node):
        """
        Adds a children.

        Input:
            node: Node - node to added in the children node list
        """
        self.Size += node.Size
        self.Children.append(node)

    def trash(self):
        """
        Makes the node invalid if the node have been used for parsing a invalid string
        """
        self.Size = 0