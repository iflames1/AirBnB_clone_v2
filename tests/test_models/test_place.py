import unittest
from models import storage
from models.city import City
from models.user import User
from models.place import Place


class TestPlace(unittest.TestCase):
    """Test the Place class"""

    @classmethod
    def setUpClass(cls):
        """Set up for test"""
        cls.user = User(email="test@example.com", password="password123")
        storage.new(cls.user)
        cls.city = City(name="San Francisco", state_id="some_state_id")
        storage.new(cls.city)
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                          name="My Place", description="Nice place")
        storage.new(cls.place)
        storage.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        storage.delete(cls.place)
        storage.delete(cls.city)
        storage.delete(cls.user)
        storage.save()

    def test_place_creation(self):
        """Test place creation"""
        place = Place(city_id=self.city.id, user_id=self.user.id,
                      name="Another Place")
        storage.new(place)
        storage.save()
        self.assertIn(place, storage.all(Place).values())
        storage.delete(place)
        storage.save()

    def test_place_attributes(self):
        """Test the attributes of the Place"""
        self.assertEqual(self.place.city_id, self.city.id)
        self.assertEqual(self.place.user_id, self.user.id)
        self.assertEqual(self.place.name, "My Place")
        self.assertEqual(self.place.description, "Nice place")


if __name__ == '__main__':
    unittest.main()
