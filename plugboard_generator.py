from sys import argv
from enum import Enum
from string import ascii_lowercase 
from json_handler import JsonHandler

INDENT = ' ' * 4

class Arguments(Enum):
    OFFSET = "-o"
    RANDOM = "-r"

class Generator():
    """Generators a json plugboard mapping."""
    ASCII_LETTER_START = 96
    def __init__(self, arg1):
        self.__arg1 = arg1
        self.__mapping = None

    def __offset_mapping(self):
        offset = 0
        try:
            offset = argv[2]
        except IndexError as e:
            offset = 1

        alphabet = list(ascii_lowercase)
        mapping = {}
        for char in alphabet:
            ascii_val = ord(char)
            new_ascii = ascii_val + offset
            if new_ascii > ord('z'):
                new_ascii = (new_ascii - ord('z') + self.ASCII_LETTER_START) 
            mapping[char] = chr(new_ascii)
        return mapping 

    def __generate_mapping(self):
        mapping = None
        if self.__arg1 == Arguments.OFFSET.value:
            mapping = self.__offset_mapping()
        handle = JsonHandler("plugboard_layout", mapping)
        handle.write()
    
    def main(self):
        self.__generate_mapping()

    @staticmethod
    def get_help():
        description = "Generates a json mapping to represent the plugboard"
        arg_help_h = "-h Displays the help page"
        arg_help_o = "-o [value] Offset generation (default: 1), where each letter "\
                     "is offset from the value given.\n e.g: offset: 1, a is mapped to b"
        arg_help_r = "-r Randomly maps each letter to another"
        print(f'{description}\n{INDENT}{arg_help_h}\n{INDENT}{arg_help_o}\n{INDENT}{arg_help_r}')





def main():
    try:
        arg1 = argv[1]
        generator = Generator(arg1)
        generator.main()
    except IndexError as e:
        Generator.get_help()




if __name__ == "__main__":
    main()
