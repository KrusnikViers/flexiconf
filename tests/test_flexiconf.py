import os
from pathlib import Path
from unittest import TestCase

from flexiconf import *
from flexiconf.utils import get_caller_path


class TestCommon(TestCase):
    test_data_dir = Path(os.path.realpath(__file__)).parent.joinpath('data')

    def test_caller_path(self):
        def constructor_frame():
            return get_caller_path()

        wanted_dir = str(self.test_data_dir.parent)
        self.assertEqual(wanted_dir, constructor_frame())

    def test_base_loader(self):
        def create_configuration():
            return Configuration([BaseLoader()])

        self.assertRaises(NotImplementedError, create_configuration)

    def test_default_path(self):
        def constructor_frame():
            config = Configuration([JsonLoader(), IniLoader()])
            self.assertEqual(5, config.get_int('b'))
            self.assertEqual(15, config.get_int('a.b.c.devalue'))

        constructor_frame()

    def test_as_dict(self):
        config = Configuration([JsonLoader(str(self.test_data_dir.joinpath('simple_1.json')))])
        self.assertEqual({"subsection": {"b": 50, "c": 3.156}, "f": "20"}, config.as_dict())

    def test_exists(self):
        config = Configuration([JsonLoader(str(self.test_data_dir.joinpath('simple_1.json')))])
        self.assertTrue(config.exists('subsection.b'))
        self.assertTrue(config.exists('f'))
        self.assertFalse(config.exists('subsection.w'))
        self.assertFalse(config.exists('z'))

    def test_json_reading(self):
        config = Configuration([JsonLoader(str(self.test_data_dir.joinpath('simple*.json')))])
        self.assertEqual(True, config.get_bool('a'))
        self.assertEqual(5, config.get_int('b'))
        self.assertEqual(3.14159, config.get_float('c'))
        self.assertEqual('some string', config.get_string('e'))
        self.assertEqual(20, config.get_int('f'))

    def test_loaders_overriding(self):
        config = Configuration([JsonLoader(str(self.test_data_dir.joinpath('simple_1.json'))),
                                JsonLoader(str(self.test_data_dir.joinpath('simple_0.json')))])
        self.assertEqual(15, config.get_int('f'))

    def test_ini_reading(self):
        config = Configuration([IniLoader(str(self.test_data_dir.joinpath('simple_0.ini')))])
        self.assertEqual('c section', config.get_string('a.b.c.value'))
        self.assertEqual(15, config.get_int('a.b.c.devalue'))
        self.assertEqual('d section', config.get_string('a.b.d.value'))
        self.assertEqual(15, config.get_int('a.b.d.devalue'))
        self.assertEqual("15", config.get('a.b.d.devalue'))

    def test_wrong_gets(self):
        config = Configuration([])

        def get_wrong_key():
            return config.get('key')

        self.assertRaises(KeyError, get_wrong_key)
        self.assertEqual("default_value", config.get('key', default="default_value"))
