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
    GAMMA = 3


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
        self.__offset = ord(start_letter.lower()) - ASCII_OFFSET
        self.__rotor_type = rotor_type

    def __increment(self):
        """Increaments the rotor offset, throws Exception if its not the alpha
        rotor."""

        if self.__rotor_type is RotorType.ALPHA:
            self.__offset += 1
        
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
        return_char = ''
        if char_pos + self.__offset > ALPHABET_LENGTH:
            pos_adjust = 0
            char_delta =  ALPHABET_LENGTH - char_pos
            offset_adjustment = self.__offset - char_delta
            # todo: Check whether this logic is valid, and why we have to
            # subtract 1
            return_char = chr(ASCII_OFFSET + offset_adjustment - 1)
        else:
            return_char = chr(ASCII_OFFSET + char_pos + self.__offset)
        self.__increment()
        return return_char


class Plugboard():
    """Simple random shift decided by the user to the map settings."""

    def __init__(self):
        self.__letter_map = {}

    def set_mapping(self, mapping):
        """Sets the letter mapping of the plug board.

        :param mapping: The mapping of a key to another
        """
        self.__letter_map = mapping
        return self.__validate()

    def __validate(self):
        """Validates the plugboard mapping is valid."""
        # This validation is trivial at best, cause we can enter invalid keys
        # of the right length to beat it, but given the plugboard mapping
        # should be randomly generated for use its not important, to validate
        # it to be robust
        if len(self.__letter_map) != 26:
            return False
        alphabet_store = list(ascii_lowercase)
        for key in self.__letter_map:
            char = self.__letter_map[key]
            try: alphabet_store.remove(char)
            except: return False
        return True

    def get_output(self, in_letter):
        """Gets the result of the char passed to the plugboard.

        :param in_letter: The letter entering the plugboard.
        """
        return self.__letter_map[in_letter]
    

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
    def __init__(self, rotor_start_positions):
    
        # Conceptually its quite confusing as the first rotor is the one on the
        # right hand side of the machine, but this is considered as the
        # 'first' rotor otherwise known as the alpha rotor
        assert(type(rotor_start_positions) is tuple)
        assert(len(rotor_start_positions) == 3)
        
        # Setting up the rotors of the machine
        self.__rotor_a = Rotor(rotor_start_positions[0], RotorType.ALPHA)
        self.__rotor_b = Rotor(rotor_start_positions[0], RotorType.BETA)
        self.__rotor_g = Rotor(rotor_start_positions[0], RotorType.GAMMA)

        self.__plugboard = Plugboard()

    def set_plugboard_mapping(self, mapping):
        """Sets the plugboard mapping.

        :param mapping: The mapping of the plug board
        """
        # Basically wraps the setter of the plugboard
        return self.__plugboard.set_mapping(mapping)

    def encrypt(self, message):
        """Encrypts the message by encrypting each character.

        :param message: The message to be encrypted
        """
        
        # Sanity checks
        assert(type(message) is str)
        encrypted = ""
        for char in message:
            encrypted = f'{encrypted}{self.__encrypt_char(char)}'
        return encrypted


    def __rotor_shift(self, char):
        """Performs the rotor shifts on a character.

        :param char: The character to be shifted
        """
        a_rotor_shift = self.__rotor_a.get_shifted_value(char)
        b_rotor_shift = self.__rotor_b.get_shifted_value(a_rotor_shift)
        return self.__rotor_g.get_shifted_value(b_rotor_shift)
    
    def __encrypt_char(self, char):
        """Encrypts a character based on the current settings.

        :param char: Character to be encrypted
        """
        plain_char = char
       
       # First pass from keyboard to plugboard
        shifted_char = self.__plugboard.get_output(plain_char)
        
        # Plugboard output to the rotors
        shifted_char = self.__rotor_shift(shifted_char)

        # Second pass from the reflector
        shifted_char = self.__rotor_shift(shifted_char)

        # Back through the plugboard to output the encrypted character
        return self.__plugboard.get_output(shifted_char)
