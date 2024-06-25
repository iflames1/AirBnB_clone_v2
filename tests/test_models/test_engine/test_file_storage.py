#!/usr/bin/python3


import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
import os
import json


class TestFileStorage(unittest.TestCase):

    def setUp(self) -> None:
        self.storage = FileStorage()
        self.file_path = self.storage._FileStorage__file_path
        self.objects = self.storage._FileStorage__objects
        self.obj = BaseModel()
        self.obj.save()

    def tearDown(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_all_returns_all_objects(self):
        """Test that all() returns all objects in storage"""
        all_objects = self.storage.all()
        self.assertIn(f'BaseModel.{self.obj.id}', all_objects)
        self.assertEqual(all_objects[f'BaseModel.{self.obj.id}'], self.obj)

    def test_all_with_class_filter(self):
        """Test that all(cls) returns objects of type cls only"""
        new_obj = BaseModel()
        new_obj.save()
        all_objects = self.storage.all(BaseModel)
        self.assertIn(f'BaseModel.{new_obj.id}', all_objects)
        new_obj_2 = BaseModel()
        new_obj_2.save()
        new_all_object = self.storage.all(BaseModel)
        self.assertIn(f'BaseModel.{self.obj.id}', all_objects)
        self.assertEqual(len(all_objects), len(new_all_object) - 1)

    def test_delete_existing_object(self):
        """Test that delete(obj) deletes obj from storage"""
        self.storage.delete(self.obj)
        all_objects_after_deletion = self.storage.all()
        self.assertNotIn(f'BaseModel.{self.obj.id}',
                         all_objects_after_deletion)

    def test_delete_existing_object2(self):
        """Test that delete(obj) deletes obj from storage"""
        obj2 = BaseModel()
        self.storage.new(obj2)
        self.storage.save()

        initial_length = len(self.storage.all())
        self.storage.delete(obj2)
        new_length = len(self.storage.all())
        self.assertEqual(new_length, initial_length - 1)

    def test_delete_none_object(self):
        """Test that delete(None) does nothing"""
        self.storage.delete(None)
        all_objects = self.storage.all()
        self.assertIn(f'BaseModel.{self.obj.id}', all_objects)

    def test_all_method(self):
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.storage.new(obj1)
        self.storage.new(obj2)
        all_object = self.storage.all()
        self.assertEqual(len(all_object), len(self.objects))
        self.assertGreaterEqual(len(all_object), 2)
        self.assertIn(obj1.__class__.__name__ + '.' + obj1.id, all_object)
        self.assertIn(obj1.__class__.__name__ + '.' + obj2.id, all_object)

    def test_new_method(self):
        obj = BaseModel()
        self.storage.new(obj)
        self.assertIn(obj.__class__.__name__ + '.' + obj.id,
                      self.storage.all())

    def test_save_method(self):
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))
        with open(self.file_path, 'r') as file:
            saved_data = json.load(file)
            self.assertIn(obj.__class__.__name__ + '.' + obj.id, saved_data)

    def test_reload_method(self):
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        self.assertIn(obj.__class__.__name__ + '.' + obj.id,
                      self.storage.all())


if __name__ == "__main__":
    unittest.main()
