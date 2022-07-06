from json import dump, load
from os import path

class JsonHandler():
    """Handles json operations including writing and loading."""

    def __init__(self, name, data):
        """Constructs a json handler instance.
 
        :param name: Name of the json file
        :param data: The json data to be written
        """
        self.__name = name
        self.__data = data
    
    def write(self, directory = ""):
        """Writes the json data to a json file.

        :param directory: The directory of the json, default to current
        directory
        """
        if directory:
            directory = fix_directory(directory)
        
        with open(f'{directory}{self.__name}.json', "w") as f:
            dump(self.__data, f, indent = 4)

    @staticmethod
    def fix_directory(directory):
        """Fixes the directory pathing .

        :param directory: The directory to be fixed
        """
        assert(type(directory) is str)
        if directory[0] != "/":
            directory = f'/{directory}'
        if directory[-1] != "/":
            directory = f'{directory}/'
        return directory

    @staticmethod
    def load(name, directory = ""):
        """Loads a json file.

        :param name: The name of the json to be loaded
        :param directory: The directory of where the json is
        """
        if directory:
            directory = fix_directory(directory)

        data = None
        with open(f'{directory}{name}', "r") as f:
            data = load(f)
        return data
