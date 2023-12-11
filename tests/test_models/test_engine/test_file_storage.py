#!/usr/bin/python3
"""defines unittests models/engine/file_storage.py.

unittest classes:
    TestFileStorage_finstantiation
    TestFileStorage_fmethods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_finstantiation(unittest.TestCase):
    """unittests for testin instantiation FileStorage class."""

    def test_FileStorage_finstantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_finstantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_ffile_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_FileStorage_fobjects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_finitializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_fmethods(unittest.TestCase):
    """unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all_f(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_fwith_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_f(self):
        fbm = BaseModel()
        fus = User()
        fst = State()
        fpl = Place()
        fcy = City()
        fam = Amenity()
        frv = Review()
        models.storage.new(fbm)
        models.storage.new(fus)
        models.storage.new(fst)
        models.storage.new(fpl)
        models.storage.new(fcy)
        models.storage.new(fam)
        models.storage.new(frv)
        self.assertIn("BaseModel." + fbm.id, models.storage.all().keys())
        self.assertIn(fbm, models.storage.all().values())
        self.assertIn("User." + fus.id, models.storage.all().keys())
        self.assertIn(fus, models.storage.all().values())
        self.assertIn("State." + fst.id, models.storage.all().keys())
        self.assertIn(fst, models.storage.all().values())
        self.assertIn("Place." + fpl.id, models.storage.all().keys())
        self.assertIn(fpl, models.storage.all().values())
        self.assertIn("City." + fcy.id, models.storage.all().keys())
        self.assertIn(fcy, models.storage.all().values())
        self.assertIn("Amenity." + fam.id, models.storage.all().keys())
        self.assertIn(fam, models.storage.all().values())
        self.assertIn("Review." + frv.id, models.storage.all().keys())
        self.assertIn(frv, models.storage.all().values())

    def test_new_fwith_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_fwith_None(self):
        # This test checks if an AttributeError is raised
        # This test checks if an AttributeError raised
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save_f(self):
        fbm = BaseModel()
        fus = User()
        fst = State()
        fpl = Place()
        fcy = City()
        fam = Amenity()
        frv = Review()
        models.storage.new(fbm)
        models.storage.new(fus)
        models.storage.new(fst)
        models.storage.new(fpl)
        models.storage.new(fcy)
        models.storage.new(fam)
        models.storage.new(frv)
        models.storage.save()
        fsave_text = ""
        with open("file.json", "r") as f:
            fsave_text = f.read()
            self.assertIn("BaseModel." + fbm.id, fsave_text)
            self.assertIn("User." + fus.id, fsave_text)
            self.assertIn("State." + fst.id, fsave_text)
            self.assertIn("Place." + fpl.id, fsave_text)
            self.assertIn("City." + fcy.id, fsave_text)
            self.assertIn("Amenity." + fam.id, fsave_text)
            self.assertIn("Review." + frv.id, fsave_text)

    def test_save_fwith_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload_f(self):
        fbm = BaseModel()
        fus = User()
        fst = State()
        fpl = Place()
        fcy = City()
        fam = Amenity()
        frv = Review()
        models.storage.new(fbm)
        models.storage.new(fus)
        models.storage.new(fst)
        models.storage.new(fpl)
        models.storage.new(fcy)
        models.storage.new(fam)
        models.storage.new(frv)
        models.storage.save()
        models.storage.reload()
        fobjs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + fbm.id, fobjs)
        self.assertIn("User." + fus.id, fobjs)
        self.assertIn("State." + fst.id, fobjs)
        self.assertIn("Place." + fpl.id, fobjs)
        self.assertIn("City." + fcy.id, fobjs)
        self.assertIn("Amenity." + fam.id, fobjs)
        self.assertIn("Review." + frv.id, fobjs)

    def test_reload_fwith_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
