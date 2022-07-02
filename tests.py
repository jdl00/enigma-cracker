from unittest import TestCase, main
from enigma_simulator import Plugboard, Rotor, RotorType

class RotorTests(TestCase):
    """Tests the rotor functionality."""

    def test_valid_alpha_rotor(self):
        """Test the alpha rotor shifts the correct value, and increments."""
        # Used to track the incrementing alpha rotor
        offset_increment = 0

        expected_value = 'd'
        rotor = Rotor('b', RotorType.ALPHA)

        # Test that before any incremements it produces the correct value
        self.assertEqual(rotor.get_shifted_value('c'), expected_value)
        offset_increment += 1

        # Because the rotor we're testing is an alpha rotor, it should
        # increment as we pass a chracter through it test this functionality
        expected_value = chr(ord(expected_value) + offset_increment)
        self.assertEqual(rotor.get_shifted_value('c'), expected_value)
        offset_increment += 1
        
        # Test the edge case of z
        expected_value = chr(ord('z') + offset_increment - 25)
        self.assertEqual(rotor.get_shifted_value('z'), expected_value)

    def test_valid_beta_gamma_rotor(self):
        """Tests that the beta and gamma rotors work as expected."""
        # Because gamma, and beta call the same code, we can just test one
        # fully and loosely test the other
        rotor = Rotor('b', RotorType.BETA)
        expected_value = 'c'
        # Tests the initial valid case
        self.assertEqual(rotor.get_shifted_value('b'), expected_value)
    
        # Tests that the offset hasn't increased 
        self.assertEqual(rotor.get_shifted_value('b'), expected_value)

        # Tests that the edge case works as expected
        expected_value = 'a'
        self.assertEqual(rotor.get_shifted_value('z'), expected_value)
        
        # Tests that the gamma rotor works the same as beta
        rotor = Rotor('b', RotorType.GAMMA)
        expected_value = 'c'
        self.assertEqual(rotor.get_shifted_value('b'), expected_value)




main(verbosity = 2)
