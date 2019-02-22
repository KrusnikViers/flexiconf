from .utils import NOT_SET, no_cast, split_key_path
from .loaders import BaseLoader


class Configuration:
    def __init__(self, loaders: list):
        self.data = dict()
        for loader in loaders:
            loader.load(self.data)

    def as_dict(self):
        return self.data

    def exists(self, key_path: str):
        parent_dict, key = self._get_dict_and_last_key(key_path)
        return bool(parent_dict) and key in parent_dict

    def set(self, key_path: str, value, override_existing=True):
        current_dict, last_key = BaseLoader.insert_path_in_dict(self.data, key_path)
        if last_key not in current_dict or override_existing:
            current_dict[last_key] = value

    def get_bool(self, key_path: str, default=NOT_SET):
        default_values = {
            "1": True, "true": True, "yes": True, "y": True, "on": True,
            "0": False, "false": False, "no": False, "n": False, "off": False,
        }
        result = self.get(key_path, default=default)
        return default_values.get(result, bool(result))

    def get_int(self, key_path: str, default=NOT_SET):
        return int(self.get(key_path, default=default))

    def get_float(self, key_path: str, default=NOT_SET):
        return float(self.get(key_path, default=default))

    def get_string(self, key_path: str, default=NOT_SET):
        return str(self.get(key_path, default=default))

    def get(self, key_path: str, cast=no_cast, default=NOT_SET):
        parent_dict, key = self._get_dict_and_last_key(key_path)
        if not parent_dict or key not in parent_dict:
            if default is NOT_SET:
                raise KeyError()
            return default
        return cast(parent_dict[key])

    def _get_dict_and_last_key(self, key_path: str):
        inner_keys, last_key = split_key_path(key_path)
        current_dict = self.data
        for key in inner_keys:
            if key in current_dict:
                current_dict = current_dict[key]
            else:
                return None, last_key
        return current_dict, last_key
