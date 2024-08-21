import unittest
from src.utils.models.types import UniverseEnum, StrategyEnum, UpdateStrategyBody


class TestTypes(unittest.TestCase):

    def test_universe_enum(self):
        """Test UniverseEnum values."""
        self.assertEqual(UniverseEnum.POKEMON.value, 'pokemon')
        self.assertEqual(UniverseEnum.SWAPI.value, 'swapi')

        # Test if UniverseEnum contains the expected values
        self.assertIn('pokemon', [e.value for e in UniverseEnum])
        self.assertIn('swapi', [e.value for e in UniverseEnum])

    def test_strategy_enum(self):
        """Test StrategyEnum values."""
        self.assertEqual(StrategyEnum.extreme_defence, 0)
        self.assertEqual(StrategyEnum.defence, 1)
        self.assertEqual(StrategyEnum.balanced, 2)
        self.assertEqual(StrategyEnum.attack, 3)
        self.assertEqual(StrategyEnum.extreme_attack, 4)

        # Test if StrategyEnum has the correct values
        self.assertIn('extreme_defence', StrategyEnum.__members__)
        self.assertIn('defence', StrategyEnum.__members__)
        self.assertIn('balanced', StrategyEnum.__members__)
        self.assertIn('attack', StrategyEnum.__members__)
        self.assertIn('extreme_attack', StrategyEnum.__members__)

    def test_update_strategy_body(self):
        """Test UpdateStrategyBody model."""
        # Valid input
        valid_data = {'strategy': 'balanced'}
        body = UpdateStrategyBody(**valid_data)
        self.assertEqual(body.strategy, 'balanced')

        # Invalid input
        with self.assertRaises(ValueError):
            UpdateStrategyBody(strategy=123)  # Strategy should be a string


if __name__ == '__main__':
    unittest.main()
