import unittest
from models import storage
from models.state import State
from models.city import City


class TestState(unittest.TestCase):
    """Test the State class"""

    @classmethod
    def setUpClass(cls):
        """Set up for test"""
        cls.state = State(name="California")
        storage.new(cls.state)
        storage.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        storage.delete(cls.state)
        storage.save()

    def test_state_creation(self):
        """Test state creation"""
        initial_count = len(storage.all(State))
        new_state = State(name="Nevada")
        storage.new(new_state)
        storage.save()
        new_count = len(storage.all(State))
        self.assertEqual(new_count, initial_count + 1)
        storage.delete(new_state)
        storage.save()
        final_count = len(storage.all(State))
        self.assertEqual(final_count, initial_count)

    def test_state_city_relationship(self):
        """Test the relationship between state and city"""
        new_city = City(name="Los Angeles", state_id=self.state.id)
        storage.new(new_city)
        storage.save()
        self.assertIn(new_city, self.state.cities)
        storage.delete(new_city)
        storage.save()


if __name__ == '__main__':
    unittest.main()
