#!/usr/bin/python3
"""Defines unittests for models/amenity.py.
Unittest classes:
    TestAmenity_sinstantiation
    TestAmenity_fsave
    TestAmenity_to_fdict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_fsinstantiation(unittest.TestCase):
    """Unittests testing instantiation of the Amenity class."""

    def test_no_args_finstantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_fstored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_fpublic_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_fpublic_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_fpublic_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_fclass_attribute(self):
        fam = Amenity()
        self.assertEqual(str,  type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", fam.__dict__)

    def test_two_amenities_funique_ids(self):
        fam1 = Amenity()
        fam2 = Amenity()
        self.assertNotEqual(fam1.id, fam2.id)

    def test_two_amenities_fdifferent_created_at(self):
        fam1 = Amenity()
        sleep(0.05)
        fam2 = Amenity()
        self.assertLess(fam1.created_at, fam2.created_at)

    def test_two_amenities_fdifferent_updated_at(self):
        fam1 = Amenity()
        sleep(0.05)
        fam2 = Amenity()
        self.assertLess(fam1.updated_at, fam2.updated_at)

    def test_str_frepresentation(self):
        fdt = datetime.today()
        fdt_repr = repr(fdt)
        fam = Amenity()
        fam.id = "123456"
        fam.created_at = fam.updated_at = fdt
        famstr = fam.__str__()
        self.assertIn("[Amenity] (123456)", famstr)
        self.assertIn("'id': '123456'", famstr)
        self.assertIn("'created_at': " + fdt_repr, famstr)
        self.assertIn("'updated_at': " + fdt_repr, famstr)

    def test_args_funused(self):
        fam = Amenity(None)
        self.assertNotIn(None, fam.__dict__.values())

    def test_instantiation_fwith_kwargs(self):
        """instantiation kwargs test method"""
        fdt = datetime.today()
        fdt_iso = fdt.isoformat()
        fam = Amenity(id="345", created_at=fdt_iso, updated_at=fdt_iso)
        self.assertEqual(fam.id, "345")
        self.assertEqual(fam.created_at, fdt)
        self.assertEqual(fam.updated_at, fdt)

    def test_instantiation_fwith_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_fsave(unittest.TestCase):
    """Unittests testing save method of the Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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
        fam = Amenity()
        sleep(0.05)
        yfirst_updated_at = fam.updated_at
        fam.save()
        self.assertLess(yfirst_updated_at, fam.updated_at)

    def test_two_fsaves(self):
        fam = Amenity()
        sleep(0.05)
        yfirst_updated_at = fam.updated_at
        fam.save()
        ysecond_updated_at = fam.updated_at
        self.assertLess(yfirst_updated_at, ysecond_updated_at)
        sleep(0.05)
        fam.save()
        self.assertLess(ysecond_updated_at, fam.updated_at)

    def test_save_fwith_arg(self):
        fam = Amenity()
        with self.assertRaises(TypeError):
            fam.save(None)

    def test_save_fupdates_file(self):
        fam = Amenity()
        fam.save()
        yamid = "Amenity." + fam.id
        with open("file.json", "r") as f:
            self.assertIn(yamid, f.read())


class TestAmenity_to_fdict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_ftype(self):
        self.assertTrue(dict,  type(Amenity().to_dict()))

    def test_to_dict_contains_correct_fkeys(self):
        fam = Amenity()
        self.assertIn("id", fam.to_dict())
        self.assertIn("created_at", fam.to_dict())
        self.assertIn("updated_at", fam.to_dict())
        self.assertIn("__class__", fam.to_dict())

    def test_to_dict_contains_added_fattributes(self):
        fam = Amenity()
        fam.middle_name = "Holberton"
        fam.my_number = 98
        self.assertEqual("Holberton", fam.middle_name)
        self.assertIn("my_number", fam.to_dict())

    def test_to_dict_datetime_attributes_are_fstrs(self):
        fam = Amenity()
        yam_dict = fam.to_dict()
        self.assertEqual(str, type(yam_dict["id"]))
        self.assertEqual(str, type(yam_dict["created_at"]))
        self.assertEqual(str, type(yam_dict["updated_at"]))

    def test_to_dict_foutput(self):
        fdt = datetime.today()
        fam = Amenity()
        fam.id = "123456"
        fam.created_at = fam.updated_at = fdt
        ytdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': fdt.isoformat(),
            'updated_at': fdt.isoformat(),
        }
        self.assertDictEqual(fam.to_dict(), ytdict)

    def test_contrast_to_dict_dunder_fdict(self):
        fam = Amenity()
        self.assertNotEqual(fam.to_dict(), fam.__dict__)

    def test_to_dict_with_farg(self):
        fam = Amenity()
        with self.assertRaises(TypeError):
            fam.to_dict(None)


if __name__ == "__main__":
    unittest.main()
