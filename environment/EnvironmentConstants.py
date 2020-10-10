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
    RDF_OUTPUT_FOLDER = ""
    OUTPUT_DIRECTORY = ""
    KNOX_18_NAMESPACE = ""
    OUTPUT_FORMAT = ""
    OUTPUT_FILE_NAME = ""
    INPUT_DIRECTORY = ""
    ERROR_DIRECTORY = ""

    def __init__(self):
        """
        Initializes the EnvironmentConstants instance
        """
        Singleton.__init__(self)
        self.INPUT_DIRECTORY = "INPUT_DIRECTORY"
        self.OUTPUT_DIRECTORY = "OUTPUT_DIRECTORY"
        self.ERROR_DIRECTORY = "ERROR_DIRECTORY"
        self.RDF_OUTPUT_FOLDER = "RDF_OUTPUT_FOLDER"
        self.KNOX_18_NAMESPACE = "KNOX_18_NAMESPACE"
        self.OUTPUT_FORMAT = "OUTPUT_FORMAT"
        self.OUTPUT_FILE_NAME = "OUTPUT_FILE_NAME"
        load_dotenv()

    def get_value(self, key: str):
        """
        Input:
            key: str - The key to loop up in the .env file

        Returns:
            str - The value for the given key
        """
        return os.environ.get(key)
        
    def get_rdf_output_folder(self):
        """
        Returns:
            str - The value stored in the environment variable "RDF_OUTPUT_FOLDER"
        """
        return os.environ.get(self.OUTPUT_DIRECTORY)
    
    def get_knox18_namespace(self):
        """
        Returns:
            str - The value stored in the environment variable "KNOX_18_NAMESPACE"
        """
        return os.environ.get(self.KNOX_18_NAMESPACE)
    
    def get_triple_output_format(self):
        """
        Returns:
            str - The value stored in the environment variable "OUTPUT_FORMAT"
        """
        return os.environ.get(self.OUTPUT_FORMAT)
    
    def get_ouput_file_name(self):
        """
        Returns:
            str - The value stored in the environment variable "OUTPUT_FILE_NAME"
        """
        return os.environ.get(self.OUTPUT_FILE_NAME)
