import unittest
from unittest.mock import Mock
from models import CreatureType, Species


class TestSpecies(unittest.TestCase):
    def setUp(self):
        self.mock_world = Mock()
        self.mock_genome = Mock()
        self.mock_genome.get_creature_type.return_value = CreatureType.HERBIVORE
        self.mock_genome.get_data.return_value = "Genome Data"

    def test_days_active_active_species(self):
        # Species created on day 0 and still active on day 10
        self.mock_world.get_day.return_value = 10
        species = Species(self.mock_genome, day=0, world=self.mock_world)
        data = species.get_data()
        self.assertEqual(data["Days Active"],10)

    def test_days_active_extinct_species(self):
        # Species created on day 0, extinct on day 5, and world is on day 10
        self.mock_world.get_day.return_value = 5
        species = Species(self.mock_genome, day=0, world=self.mock_world)
        species._population = 1
        species.dec_population()  # day_extinct is 5
        self.mock_world.get_day.return_value = 10
        data = species.get_data()
        self.assertEqual(data["Days Active"],5)

    def test_days_active_extinct_and_reactivated_species(self):
        # Species created on day 0, goes extinct on day 5, then becomes active again on day 8
        self.mock_world.get_day.return_value = 5
        species = Species(self.mock_genome, day=0, world=self.mock_world)
        species._population = 1
        species.dec_population()  # extinct on day 5

        # Species active day 8
        self.mock_world.get_day.return_value = 8
        species.inc_population()  # update _days_extinct

        # World day 10
        self.mock_world.get_day.return_value = 10
        data = species.get_data()
        # Expected Days Active = 5 (initial) + 2 (after)
        self.assertEqual(data["Days Active"], 7)

    def test_multiple_extinction_species(self):
        # Species created on day 0, goes extinct on day 5, then becomes active again on day 8
        self.mock_world.get_day.return_value = 5
        species = Species(self.mock_genome, day=0, world=self.mock_world)
        species._population = 1
        species.dec_population()  # extinct on day 5

        # Species active day 8
        self.mock_world.get_day.return_value = 8
        species.inc_population()  # reset _days_extinct

        # World day 10
        self.mock_world.get_day.return_value = 10
        species.dec_population()  # extinct

        self.mock_world.get_day.return_value = 20
        species.inc_population() # reset _days_extinct
        self.mock_world.get_day.return_value = 30
        data = species.get_data()
        # Expected Days Active = 5 (initial) + 2 (after) + 10 (after)
        self.assertEqual(data["Days Active"], 17)


if __name__ == "__main__":
    unittest.main()
