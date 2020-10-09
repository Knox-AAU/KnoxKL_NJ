from dotenv import load_dotenv
import os

class Singleton:
    """
    Basic Singleton class that can be inherited from for creating classes in the singleton pattern.
    Allows only for a single instance of the class to exist at a time
    """
    _shared_state = {}
    def __init__(self):
        """
        Saves the state of the singleton to ensure only a single version of the instance exist
        """
        self.__dict__ = self._shared_state

class EnvironmentConstants(Singleton):
    """
    Singleton instance for accessing the values stored in the environment variables for the project
    """
    def __init__(self):
        """
        Initializes the EnvironmentConstants instance
        """
        Singleton.__init__(self)
        self.RDF_OUTPUT_FOLDER = "RDF_OUTPUT_FOLDER"
        self.KNOX_18_NAMESPACE = "KNOX_18_NAMESPACE"
        self.OUTPUT_FORMAT = "OUTPUT_FORMAT"
        self.OUTPUT_FILE_NAME = "OUTPUT_FILE_NAME"
        load_dotenv()
        
    def getRDFOutputFolder(self):
        """
        Returns:
            str - The value stored in the environment variable "RDF_OUTPUT_FOLDER"
        """
        return os.environ.get(self.RDF_OUTPUT_FOLDER)
    
    def getKnox18Namespace(self):
        """
        Returns:
            str - The value stored in the environment variable "KNOX_18_NAMESPACE"
        """
        return os.environ.get(self.KNOX_18_NAMESPACE)
    
    def getTripleOutputFormat(self):
        """
        Returns:
            str - The value stored in the environment variable "OUTPUT_FORMAT"
        """
        return os.environ.get(self.OUTPUT_FORMAT)
    
    def getOutputFileName(self):
        """
        Returns:
            str - The value stored in the environment variable "OUTPUT_FILE_NAME"
        """
        return os.environ.get(self.OUTPUT_FILE_NAME)