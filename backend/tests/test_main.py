import unittest
from fastapi.testclient import TestClient
from main import app, current_teams
from src.utils.models.types import UniverseEnum, UpdateStrategyBody
from src.utils.helpers import create_team, get_team, replace_team, change_team_strategy


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Clear current_teams before each test
        current_teams.clear()

    def test_get_pokemon_team(self):
        """Test GET /api/poketeam endpoint."""
        # Create a team to ensure there is data to retrieve
        self.client.post("/api/poketeam")
        response = self.client.get("/api/poketeam")
        self.assertEqual(response.status_code, 200)
        self.assertIn('goalie', response.json())
        self.assertIn('attackers', response.json())
        self.assertIn('defenders', response.json())

    def test_create_pokemon_team(self):
        """Test POST /api/poketeam endpoint."""
        response = self.client.post("/api/poketeam")
        self.assertEqual(response.status_code, 200)
        self.assertIn('goalie', response.json())
        self.assertIn('attackers', response.json())
        self.assertIn('defenders', response.json())

    def test_replace_pokemon_team(self):
        """Test PUT /api/poketeam endpoint."""
        self.client.post("/api/poketeam")  # Create a team first
        response = self.client.put("/api/poketeam")
        self.assertEqual(response.status_code, 200)
        self.assertIn('goalie', response.json())
        self.assertIn('attackers', response.json())
        self.assertIn('defenders', response.json())

    def test_change_pokemon_strategy(self):
        """Test PATCH /api/poketeam/strategy endpoint."""
        self.client.post("/api/poketeam")  # Create a team first
        response = self.client.patch(
            "/api/poketeam/strategy", json={"strategy": "attack"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['goalie'], response.json().get('goalie'))

    def test_get_star_wars_team(self):
        """Test GET /api/swteam endpoint."""
        # Create a Star Wars team to ensure there is data to retrieve
        self.client.post("/api/swteam")
        response = self.client.get("/api/swteam")
        self.assertEqual(response.status_code, 200)
        self.assertIn('goalie', response.json())
        self.assertIn('attackers', response.json())
        self.assertIn('defenders', response.json())

    def test_create_star_wars_team(self):
        """Test POST /api/swteam endpoint."""
        response = self.client.post("/api/swteam")
        self.assertEqual(response.status_code, 200)
        self.assertIn('goalie', response.json())
        self.assertIn('attackers', response.json())
        self.assertIn('defenders', response.json())

    def test_replace_star_wars_team(self):
        """Test PUT /api/swteam endpoint."""
        self.client.post("/api/swteam")  # Create a team first
        response = self.client.put("/api/swteam")
        self.assertEqual(response.status_code, 200)
        self.assertIn('goalie', response.json())
        self.assertIn('attackers', response.json())
        self.assertIn('defenders', response.json())

    def test_change_star_wars_strategy(self):
        """Test PATCH /api/swteam/strategy endpoint."""
        self.client.post("/api/swteam")  # Create a team first
        response = self.client.patch(
            "/api/swteam/strategy", json={"strategy": "attack"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['goalie'], response.json().get('goalie'))


if __name__ == '__main__':
    unittest.main()
