#!/usr/bin/python3
"""defines unittests models/base_model.py.

Unittest classes:
    TestBaseModel_finstantiation
    TestBaseModel_fsave
    TestBaseModel_to_fdict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_finstantiation(unittest.TestCase):
    """Unittests testing instantiation the BaseModel class."""

    def test_no_args_finstantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_fobjects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_fstr(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_fdatetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_fdatetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_fids(self):
        fbm1 = BaseModel()
        fbm2 = BaseModel()
        self.assertNotEqual(fbm1.id, fbm2.id)

    def test_two_models_different_created_fat(self):
        fbm1 = BaseModel()
        sleep(0.05)
        fbm2 = BaseModel()
        self.assertLess(fbm1.created_at, fbm2.created_at)

    def test_two_models_different_updated_fat(self):
        fbm1 = BaseModel()
        sleep(0.05)
        fbm2 = BaseModel()
        self.assertLess(fbm1.updated_at, fbm2.updated_at)

    def test_str_frepresentation(self):
        fdt = datetime.today()
        fdt_repr = repr(fdt)
        fbm = BaseModel()
        fbm.id = "123456"
        fbm.created_at = fbm.updated_at = fdt
        ybmstr = fbm.__str__()
        self.assertIn("[BaseModel] (123456)", ybmstr)
        self.assertIn("'id': '123456'", ybmstr)
        self.assertIn("'created_at': " + fdt_repr, ybmstr)
        self.assertIn("'updated_at': " + fdt_repr, ybmstr)

    def test_args_funused(self):
        fbm = BaseModel(None)
        self.assertNotIn(None, fbm.__dict__.values())

    def test_instantiation_with_fkwargs(self):
        fdt = datetime.today()
        dt_iso = fdt.isoformat()
        fbm = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(fbm.id, "345")
        self.assertEqual(fbm.created_at, fdt)
        self.assertEqual(fbm.updated_at, fdt)

    def test_instantiation_with_None_fkwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_fkwargs(self):
        fdt = datetime.today()
        dt_iso = fdt.isoformat()
        fbm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(fbm.id, "345")
        self.assertEqual(fbm.created_at, fdt)
        self.assertEqual(fbm.updated_at, fdt)


class TestBaseModel_fsave(unittest.TestCase):
    """Unittests testing BaseModel class."""

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

    def test_one_fsave(self):
        fbm = BaseModel()
        sleep(0.05)
        yfirst_updated_at = fbm.updated_at
        fbm.save()
        self.assertLess(yfirst_updated_at, fbm.updated_at)

    def test_two_fsaves(self):
        fbm = BaseModel()
        sleep(0.05)
        yfirst_updated_at = fbm.updated_at
        fbm.save()
        ysecond_updated_at = fbm.updated_at
        self.assertLess(yfirst_updated_at, ysecond_updated_at)
        sleep(0.05)
        fbm.save()
        self.assertLess(ysecond_updated_at, fbm.updated_at)

    def test_save_fwith_arg(self):
        fbm = BaseModel()
        with self.assertRaises(TypeError):
            fbm.save(None)

    def test_save_fupdates_file(self):
        fbm = BaseModel()
        fbm.save()
        ybmid = "BaseModel." + fbm.id
        with open("file.json", "r") as f:
            self.assertIn(ybmid, f.read())


class TestBaseModel_to_fdict(unittest.TestCase):
    """Unittests testing to_dict method of the BaseModel class."""

    def test_to_fdict_type(self):
        fbm = BaseModel()
        self.assertTrue(dict, type(fbm.to_dict()))

    def test_to_dict_fcontains_correct_keys(self):
        fbm = BaseModel()
        self.assertIn("id", fbm.to_dict())
        self.assertIn("created_at", fbm.to_dict())
        self.assertIn("updated_at", fbm.to_dict())
        self.assertIn("__class__", fbm.to_dict())

    def test_to_dict_fcontains_added_attributes(self):
        fbm = BaseModel()
        fbm.name = "Holberton"
        fbm.my_number = 98
        self.assertIn("name", fbm.to_dict())
        self.assertIn("my_number", fbm.to_dict())

    def test_to_dict_datetime_fattributes_are_strs(self):
        fbm = BaseModel()
        bm_dict = fbm.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_foutput(self):
        fdt = datetime.today()
        fbm = BaseModel()
        fbm.id = "123456"
        fbm.created_at = fbm.updated_at = fdt
        ytdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': fdt.isoformat(),
            'updated_at': fdt.isoformat()
        }
        self.assertDictEqual(fbm.to_dict(), ytdict)

    def test_contrast_to_dict_fdunder_dict(self):
        fbm = BaseModel()
        self.assertNotEqual(fbm.to_dict(), fbm.__dict__)

    def test_to_dict_fwith_arg(self):
        fbm = BaseModel()
        with self.assertRaises(TypeError):
            fbm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
