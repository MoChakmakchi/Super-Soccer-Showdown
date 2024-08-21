import unittest
from src.entities.player import Player

class TestPlayer(unittest.TestCase):
    
    def test_valid_initialization(self):
        player = Player("Alice", 70.0, 1.75)
        self.assertEqual(player.name, "Alice", "Name should be 'Alice'")
        self.assertEqual(player.weight, 70.0, "Weight should be 70.0")
        self.assertEqual(player.height, 1.75, "Height should be 1.75")

    def test_negative_weight(self):
        print("Running test_negative_weight...")
        with self.assertRaises(ValueError) as context:
            Player("Bob", -70.0, 1.75)
        self.assertEqual(str(context.exception), "Weight and height must be non-negative.", "Exception message should be about non-negative values.")

    def test_negative_height(self):
        print("Running test_negative_height...")
        with self.assertRaises(ValueError) as context:
            Player("Charlie", 70.0, -1.75)
        self.assertEqual(str(context.exception), "Weight and height must be non-negative.", "Exception message should be about non-negative values.")

    def test_negative_weight_and_height(self):
        print("Running test_negative_weight_and_height...")
        with self.assertRaises(ValueError) as context:
            Player("Diana", -70.0, -1.75)
        self.assertEqual(str(context.exception), "Weight and height must be non-negative.", "Exception message should be about non-negative values.")
    
    def test_zero_weight_and_height(self):
        print("Running test_zero_weight_and_height...")
        player = Player("Eve", 0.0, 0.0)
        self.assertEqual(player.name, "Eve", "Name should be 'Eve'")
        self.assertEqual(player.weight, 0.0, "Weight should be 0.0")
        self.assertEqual(player.height, 0.0, "Height should be 0.0")
    
    def test_valid_edge_cases(self):
        # TODO: add more specific edge cases to test
        print("Running test_valid_edge_cases...")

if __name__ == '__main__':
    unittest.main()
