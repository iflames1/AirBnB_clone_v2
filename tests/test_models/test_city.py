import unittest
from models import storage
from models.state import State
from models.city import City


class TestCity(unittest.TestCase):
    """Test the City class"""

    @classmethod
    def setUpClass(cls):
        """Set up for test"""
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)
        storage.new(cls.state)
        storage.new(cls.city)
        storage.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        storage.delete(cls.city)
        storage.delete(cls.state)
        storage.save()

    def test_city_creation(self):
        """Test city creation"""
        initial_count = len(storage.all(City))
        new_city = City(name="Los Angeles", state_id=self.state.id)
        storage.new(new_city)
        storage.save()
        new_count = len(storage.all(City))
        self.assertEqual(new_count, initial_count + 1)
        storage.delete(new_city)
        storage.save()
        final_count = len(storage.all(City))
        self.assertEqual(final_count, initial_count)

    def test_city_state_relationship(self):
        """Test the relationship between city and state"""
        self.assertEqual(self.city.state_id, self.state.id)


if __name__ == '__main__':
    unittest.main()
