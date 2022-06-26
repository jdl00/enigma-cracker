"""
References:
    1) By MesserWoland - Own work based on: File:Enigma-action.png by User:Jeanot; original diagram by Matt Crypto, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1794494
"""

"""
Diagram help:

* First character represents the digit inputted on each rotor
|a|
|b|
|c|
|d|
offset of 0
|b|
|c|
|d|
|e|
offset of 1
"""

# Std library imports
from enum import Enum
from string import ascii_lowercase

ASCII_OFFSET = 97
ALPHABET_LENGTH = 25

class RotorType(Enum):
    ALPHA = 1 
    BETA = 2
    GAMA = 3


class Rotor():
    """Class representing a rotor on an engima machine."""

    def __init__(self, start_letter, rotor_type):
        """Sets up an instance of rotor, and returns it.

        :param start_letter: The letter selected on the rotor
        """
        # Asserts for sanity checks
        assert(isinstance(rotor_type, RotorType))
        assert(isinstance(start_letter, str))

        # The offset is the displacement from the start letter to a it should
        # only change, for the first rotor, as it's reflected back
        self.__offset = ord(start_letter) - ASCII_OFFSET
        self.__rotor_type = rotor_type

    def increment(self):
        """Increaments the rotor offset, throws Exception if its not the alpha
        rotor."""

        if self.__rotor_type is RotorType.ALPHA:
            self.__offset += 1
        else:
            raise Exception (f'Attempted to increment invalid rotor:'\
                             f'{self.__rotor.name}')

    def debug(self):
        print(f'offset: {self.__offset}')

    def get_shifted_value(self, input_char):
        """Gets the output of the roto.

        :param input_char: The char thats been entered to the rotor
        """

        # Asserts for sanity checks
        assert(isinstance(input_char, str))

        # Get the char position relative to ord('a') == ASCII_OFFSET
        char_pos = ord(input_char.lower()) - ASCII_OFFSET
        
        # If the input char, takes us beyond 25 adjust offset, as 'a' is equal
        # to 0
        if char_pos + self.__offset > ALPHABET_LENGTH:
            pos_adjust = 0
            char_delta =  ALPHABET_LENGTH - char_pos
            print(f'char delta: {char_delta}')
            offset_adjustment = self.__offset - char_delta
            print(f'offset adjustment {offset_adjustment}')
            # todo: Check whether this logic is valid, and why we have to
            # subtract 1
            return chr(ASCII_OFFSET + offset_adjustment - 1)
        else:
            return chr(ASCII_OFFSET + char_pos + self.__offset)


class Plugboard():
    """Simple random shift decided by the user to the map settings."""

    def __init__(self):
        self.__letter_map = {}
        


# Clarifications:
#   - Machine is based on a single stepping rotation
#       - The chosen rotor is the first 
#   - Within the plugboard, all letters must be plugged into another
class EnigmaMachine():
    """
    Attemps to simulate the enigma machine, 
    used by the Germans in WW2, later 
    broken the team at Bletchley Park led 
    by Alan Turning. It attempts to simulate 
    the rotor designs and pathways as shown 
    in reference 1
    """



# Driver testing code
def main():
    alpha_rotor = Rotor("k", RotorType.ALPHA)
    for i in range(22):
        print(alpha_rotor.get_shifted_value("c"))
        alpha_rotor.increment()



if __name__ == "__main__":
    main()
































