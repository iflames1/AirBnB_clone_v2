import unittest
from models import storage
from models.user import User


class TestUser(unittest.TestCase):
    """Test the User class"""

    @classmethod
    def setUpClass(cls):
        """Set up for test"""
        cls.user = User(
            email="test@example.com", password="password123",
            first_name="Test", last_name="User")
        storage.new(cls.user)
        storage.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        storage.delete(cls.user)
        storage.save()

    def test_user_creation(self):
        """Test user creation"""
        initial_count = len(storage.all(User))
        new_user = User(
            email="new@example.com", password="newpassword123",
            first_name="New", last_name="User")
        storage.new(new_user)
        storage.save()
        new_count = len(storage.all(User))
        self.assertEqual(new_count, initial_count + 1)
        storage.delete(new_user)
        storage.save()
        final_count = len(storage.all(User))
        self.assertEqual(final_count, initial_count)

    def test_user_attributes(self):
        """Test the attributes of the User"""
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.password, "password123")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")

    def test_user_update(self):
        """Test updating user attributes"""
        self.user.first_name = "Updated"
        self.user.last_name = "Name"
        storage.save()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")

    def test_user_deletion(self):
        """Test user deletion"""
        initial_count = len(storage.all(User))
        user_to_delete = User(
            email="delete@example.com", password="deletepassword123",
            first_name="Delete", last_name="User")
        storage.new(user_to_delete)
        storage.save()
        storage.delete(user_to_delete)
        storage.save()
        final_count = len(storage.all(User))
        self.assertEqual(final_count, initial_count)


if __name__ == '__main__':
    unittest.main()
