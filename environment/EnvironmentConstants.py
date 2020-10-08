from dotenv import load_dotenv
import os

class Singleton:
    '''
    Basic Singleton class that can be inherited from for creating classes in the singleton pattern.
    Allows only for a single instance of the class to exist at a time
    '''
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class EnvironmentConstants(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self.RDF_OUTPUT_FOLDER = "RDF_OUTPUT_FOLDER"
        self.KNOX_18_NAMESPACE = "KNOX_18_NAMESPACE"
        self.OUTPUT_FORMAT = "OUTPUT_FORMAT"
        self.OUTPUT_FILE_NAME = "OUTPUT_FILE_NAME"
        load_dotenv()
        
    def getRDFOutputFolder(self):
        return os.environ.get(self.RDF_OUTPUT_FOLDER)
    
    def getKnox18Namespace(self):
        return os.environ.get(self.KNOX_18_NAMESPACE)
    
    def getTripleOutputFormat(self):
        return os.environ.get(self.OUTPUT_FORMAT)
    
    def getOutputFileName(self):
        return os.environ.get(self.OUTPUT_FILE_NAME)