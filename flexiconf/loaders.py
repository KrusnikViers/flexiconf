import configparser
import glob
import json
from os import path

from .utils import NOT_SET, get_caller_path, split_key_path


class BaseLoader:
    def __init__(self):
        pass

    def load(self, config_data: dict):
        raise NotImplementedError()

    @staticmethod
    def insert_path_in_dict(data: dict, key_path: str):
        inner_keys, last_key = split_key_path(key_path)
        current_dict = data
        for key in inner_keys:
            if key not in current_dict or not isinstance(current_dict[key], dict):
                current_dict[key] = dict()
            current_dict = current_dict[key]
        return current_dict, last_key

    @staticmethod
    def enumerate_files(config_files_pattern: str):
        return [filename for filename in glob.iglob(config_files_pattern, recursive=True) if path.isfile(filename)]

    @staticmethod
    def normalize_dict(data: dict):
        return {key.lower(): value for key, value in data.items()}


class JsonLoader(BaseLoader):
    def __init__(self, config_files_pattern: str = NOT_SET):
        super(JsonLoader, self).__init__()
        if config_files_pattern is NOT_SET:
            config_files_pattern = path.join(get_caller_path(), '**/*.json')
        self.files_pattern = config_files_pattern

    def load(self, config_data: dict):
        files_list = self.enumerate_files(self.files_pattern)
        for file in files_list:
            with open(file) as json_file:
                new_data = json.load(json_file)
                new_data = self.normalize_dict(new_data)
                config_data.update(new_data)


class ConfigLoader(BaseLoader):
    def __init__(self, config_files_pattern: str = NOT_SET):
        super(ConfigLoader, self).__init__()
        if config_files_pattern is NOT_SET:
            config_files_pattern = path.join(get_caller_path(), '**/*.ini')
        self.files_pattern = config_files_pattern

    def load(self, config_data: dict):
        files_list = self.enumerate_files(self.files_pattern)
        for file in files_list:
            config = configparser.ConfigParser()
            config.read(file)
            for section_name in config.sections():
                section_dict, _ = self.insert_path_in_dict(config_data, section_name + '._')
                read_section = self.normalize_dict(dict(config[section_name]))
                section_dict.update(read_section)
