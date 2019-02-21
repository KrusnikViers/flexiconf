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
        config = Configuration([ConfigLoader(str(self.test_data_dir.joinpath('simple_0.ini')))])
        self.assertEqual('c section', config.get_string('a.b.c.value'))
        self.assertEqual(15, config.get_int('a.b.c.devalue'))
        self.assertEqual('d section', config.get_string('a.b.d.value'))
        self.assertEqual(15, config.get_int('a.b.d.devalue'))
        self.assertEqual("15", config.get('a.b.d.devalue'))
