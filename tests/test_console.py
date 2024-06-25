#!/usr/bin/python3

import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User


class TestHBNBCommand(unittest.TestCase):
    """Unit tests for the HBNBCommand class"""

    def setUp(self):
        """Set up for the tests"""
        self.console = HBNBCommand()

    def tearDown(self):
        """Tear down for the tests"""
        storage.reload()

    def test_help(self):
        """Test the help command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("help")
            output = f.getvalue()
        self.assertIsNotNone(output)

    def test_all(self):
        """Test all command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all User")
            output = f.getvalue().strip()
        self.assertIn(user_id, output)

    def test_all_invalid_class(self):
        """Test all command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all NonExistentClass")
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_create(self):
        """Test create command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()
            self.assertIsNotNone(user_id)

    def test_create_missing_class(self):
        """Test create command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            output = f.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    def test_create_invalid_class(self):
        """Test create command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create NonExistentClass")
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_create_valid_class_with_parameters(self):
        """Test create command with valid class name and parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            state_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show State {state_id}")
            output = f.getvalue().strip()
        self.assertIn("California", output)

    def test_create_valid_class_with_multiple_parameters(self):
        """Test create command with valid class name and multiple parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(
                """create Place city_id="0001" user_id="0001"
                name="My_little_house" '
                'number_rooms=4 number_bathrooms=2 max_guest=10
                price_by_night=300 '
                'latitude=37.773972 longitude=-122.431297"""
                )
            place_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show Place {place_id}")
            output = f.getvalue().strip()
        self.assertIn("My little house", output)
        self.assertIn("number_rooms", output)
        self.assertIn("number_bathrooms", output)
        self.assertIn("max_guest", output)
        self.assertIn("price_by_night", output)
        self.assertIn("latitude", output)
        self.assertIn("longitude", output)

    def test_create_with_underscore_in_string(self):
        """Test create command with underscores in string parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create Place name="My_little_house"')
            place_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show Place {place_id}")
            output = f.getvalue().strip()
        self.assertIn("My little house", output)

    def test_show(self):
        """Test show command"""
        # Create a User instance first
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show User {user_id}")
            output = f.getvalue().strip()
        self.assertIn(user_id, output)

    def test_show_missing_class(self):
        """Test show command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            output = f.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    def test_show_missing_id(self):
        """Test show command with missing instance id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show User")
            output = f.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

    def test_show_invalid_class(self):
        """Test show command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show NonExistentClass 1234")
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_show_no_instance(self):
        """Test show command with non-existing instance id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show User 1234")
            output = f.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_destroy(self):
        """Test destroy command"""
        # Create a User instance first
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"destroy User {user_id}")
            output = f.getvalue().strip()
        self.assertEqual(output, "")

        # Try to show the destroyed instance
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show User {user_id}")
            output = f.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_destroy_missing_class(self):
        """Test destroy command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy")
            output = f.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    def test_destroy_missing_id(self):
        """Test destroy command with missing instance id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy User")
            output = f.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

    def test_destroy_invalid_class(self):
        """Test destroy command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy NonExistentClass 1234")
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_destroy_no_instance(self):
        """Test destroy command with non-existing instance id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy User 1234")
            output = f.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_count(self):
        """Test count command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id1 = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id2 = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("count User")
            output = f.getvalue().strip()
        count = sum(1 for key in storage.all().keys()
                    if key.startswith("User" + "."))
        self.assertEqual(output, str(count))

    def test_count_missing_class(self):
        """Test count command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("count")
            output = f.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    def test_count_invalid_class(self):
        """Test count command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("count NonExistentClass")
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_update(self):
        """Test update command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'update User {user_id} first_name "John"')
            output = f.getvalue().strip()
        self.assertEqual(output, "")

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show User {user_id}")
            output = f.getvalue().strip()
        self.assertIn("'first_name': 'John'", output)

    def test_update_integer(self):
        """Test update command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'update User {user_id} max_guest 7')
            output = f.getvalue().strip()
        self.assertEqual(output, "")

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show User {user_id}")
            output = f.getvalue().strip()
        self.assertIn("'max_guest': 7", output)

    def test_update_missing_class(self):
        """Test update command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            output = f.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    def test_update_invalid_class(self):
        """Test update command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update NonExistentClass 1234")
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_update_missing_id(self):
        """Test update command with missing instance id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User")
            output = f.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

    def test_update_no_instance(self):
        """Test update command with non-existing instance id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User 1234")
            output = f.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_update_missing_attr_name(self):
        """Test update command with missing attribute name"""
        # create a User
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"update User {user_id}")
            output = f.getvalue().strip()
        self.assertEqual(output, "** attribute name missing **")

    """This test was intentional made to fail."""
    def test_update_missing_value(self):
        """Test update command with missing value"""
        # create a User
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"update User {user_id} first_name")
            output = f.getvalue().strip()
        self.assertEqual(output, "** value missing **")


if __name__ == "__main__":
    unittest.main()
