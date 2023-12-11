#!/usr/bin/python3
"""Defines unittests for models/state.py.

Unittest classes:
    TestState_finstantiation
    TestState_fsave
    TestState_to_fdict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_finstantiation(unittest.TestCase):
    """Unittests to test instantiation of State class."""

    def test_no_args_finstantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_fstored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_fpublic_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_fpublic_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_fpublic_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_fclass_attribute(self):
        yst = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(yst))
        self.assertNotIn("name", yst.__dict__)

    def test_two_states_funique_ids(self):
        st1 = State()
        st2 = State()
        self.assertNotEqual(st1.id, st2.id)

    def test_two_states_fdifferent_created_at(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.created_at, st2.created_at)

    def test_two_states_fdifferent_updated_at(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.updated_at, st2.updated_at)

    def test_str_frepresentation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        yst = State()
        yst.id = "123456"
        yst.created_at = yst.updated_at = dt
        ststr = yst.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + dt_repr, ststr)
        self.assertIn("'updated_at': " + dt_repr, ststr)

    def test_args_funused(self):
        yst = State(None)
        self.assertNotIn(None, yst.__dict__.values())

    def test_instantiation_fwith_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        yst = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(yst.id, "345")
        self.assertEqual(yst.created_at, dt)
        self.assertEqual(yst.updated_at, dt)

    def test_instantiation_with_fNone_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_fsave(unittest.TestCase):
    """Unittests for test save method of State class."""

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
        yst = State()
        sleep(0.05)
        yfirst_updated_at = yst.updated_at
        yst.save()
        self.assertLess(yfirst_updated_at, yst.updated_at)

    def test_two_fsaves(self):
        yst = State()
        sleep(0.05)
        yfirst_updated_at = yst.updated_at
        yst.save()
        second_updated_at = yst.updated_at
        self.assertLess(yfirst_updated_at, second_updated_at)
        sleep(0.05)
        yst.save()
        self.assertLess(second_updated_at, yst.updated_at)

    def test_save_fwith_arg(self):
        yst = State()
        with self.assertRaises(TypeError):
            yst.save(None)

    def test_save_fupdates_file(self):
        yst = State()
        yst.save()
        ystid = "State." + yst.id
        with open("file.json", "r") as f:
            self.assertIn(ystid, f.read())


class TestState_to_fdict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_to_dict_ftype(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_fcorrect_keys(self):
        yst = State()
        self.assertIn("id", yst.to_dict())
        self.assertIn("created_at", yst.to_dict())
        self.assertIn("updated_at", yst.to_dict())
        self.assertIn("__class__", yst.to_dict())

    def test_to_dict_contains_added_fattributes(self):
        yst = State()
        yst.middle_name = "Holberton"
        yst.my_number = 98
        self.assertEqual("Holberton", yst.middle_name)
        self.assertIn("my_number", yst.to_dict())

    def test_to_dict_datetime_fattributes_are_strs(self):
        yst = State()
        st_dict = yst.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def test_to_dict_foutput(self):
        dt = datetime.today()
        yst = State()
        yst.id = "123456"
        yst.created_at = yst.updated_at = dt
        ytdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(yst.to_dict(), ytdict)

    def test_contrast_to_fdict_dunder_dict(self):
        yst = State()
        self.assertNotEqual(yst.to_dict(), yst.__dict__)

    def test_to_dict_fwith_arg(self):
        yst = State()
        with self.assertRaises(TypeError):
            yst.to_dict(None)


if __name__ == "__main__":
    unittest.main()
