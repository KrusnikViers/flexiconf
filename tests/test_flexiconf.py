import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

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

    def test_set(self):
        config = Configuration([JsonLoader(str(self.test_data_dir.joinpath('simple_1.json')))])
        self.assertEqual({"subsection": {"b": 50, "c": 3.156}, "f": "20"}, config.as_dict())
        config.set('z.w.u', 20)
        config.set('subsection.b', 120, override_existing=False)
        config.set('subsection.c', 120)
        self.assertEqual({"subsection": {"b": 50, "c": 120}, "f": "20", "z": {"w": {"u": 20}}}, config.as_dict())

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

    @patch('sys.argv', ['_', '--just-flag', 'A=15', '--b.C=test'])
    def test_args_reading(self):
        config = Configuration([ArgsLoader()])
        self.assertEqual({'a': '15', 'b': {'c': 'test'}}, config.as_dict())

    @patch('os.environ', {'FCONF_A': 'env_a', 'FCONF_B': '15', 'PATH': 'path1;path2'})
    def test_env_reading(self):
        config = Configuration([EnvLoader('FCONF_.*')])
        self.assertEqual({'fconf_a': 'env_a', 'fconf_b': '15'}, config.as_dict())

    def test_wrong_gets(self):
        config = Configuration([])
        self.assertRaises(KeyError, lambda: config.get('key'))
        self.assertRaises(KeyError, lambda: config.get('a.b.c.key'))
        self.assertEqual("default_value", config.get('key', default="default_value"))
