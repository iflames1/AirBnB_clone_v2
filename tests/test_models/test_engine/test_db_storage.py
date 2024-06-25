import unittest
from models import storage
from models.state import State
from models.city import City
from models.user import User


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

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

    def test_all(self):
        """Test the all method"""
        all_objs = storage.all()
        self.assertIn(f'State.{self.state.id}', all_objs)
        self.assertIn(f'City.{self.city.id}', all_objs)

    def test_new(self):
        """Test the new method"""
        new_state = State(name="Nevada")
        storage.new(new_state)
        storage.save()
        all_objs = storage.all(State)
        self.assertIn(f'State.{new_state.id}', all_objs)
        storage.delete(new_state)
        storage.save()

    def test_save(self):
        """Test the save method"""
        new_state = State(name="Texas")
        storage.new(new_state)
        storage.save()
        all_objs = storage.all(State)
        self.assertIn(f'State.{new_state.id}', all_objs)
        storage.delete(new_state)
        storage.save()

    def test_delete(self):
        """Test the delete method"""
        new_state = State(name="Arizona")
        storage.new(new_state)
        storage.save()
        storage.delete(new_state)
        storage.save()
        all_objs = storage.all(State)
        self.assertNotIn(f'State.{new_state.id}', all_objs)

    def test_reload(self):
        """Test the reload method"""
        storage.reload()
        all_objs = storage.all()
        self.assertIn(f'State.{self.state.id}', all_objs)
        self.assertIn(f'City.{self.city.id}', all_objs)

    def test_all_with_cls(self):
        """Test the all method with class filter"""
        all_states = storage.all(State)
        all_cities = storage.all(City)
        self.assertIn(f'State.{self.state.id}', all_states)
        self.assertNotIn(f'City.{self.city.id}', all_states)
        self.assertIn(f'City.{self.city.id}', all_cities)

    def test_state_count(self):
        """Test the count of states before and after adding a new state"""
        initial_count = len(storage.all(State))
        new_state = State(name="Washington")
        storage.new(new_state)
        storage.save()
        new_count = len(storage.all(State))
        self.assertEqual(new_count, initial_count + 1)
        storage.delete(new_state)
        storage.save()
        final_count = len(storage.all(State))
        self.assertEqual(final_count, initial_count)

    def test_user_creation(self):
        """Test user creation"""
        initial_count = len(storage.all(User))
        new_user = User(email="newuser@example.com", password="newpassword")
        storage.new(new_user)
        storage.save()
        new_count = len(storage.all(User))
        self.assertEqual(new_count, initial_count + 1)
        storage.delete(new_user)
        storage.save()
        final_count = len(storage.all(User))
        self.assertEqual(final_count, initial_count)


if __name__ == '__main__':
    unittest.main()
