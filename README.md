# flexiconf
Simple and flexible separation settings from code

[![Build Status](https://travis-ci.org/KrusnikViers/flexiconf.svg?branch=master)](https://travis-ci.org/KrusnikViers/flexiconf)
[![codecov](https://codecov.io/gh/KrusnikViers/flexiconf/branch/master/graph/badge.svg)](https://codecov.io/gh/KrusnikViers/flexiconf)
[![PyPI version](https://badge.fury.io/py/flexiconf.svg)](https://badge.fury.io/py/flexiconf)
[![Maintainability](https://api.codeclimate.com/v1/badges/f947f0c596656595854f/maintainability)](https://codeclimate.com/github/KrusnikViers/flexiconf/maintainability)

Install: `pip install flexiconf`

## How to use:
### Config creation:
```
import flexiconf
config = flexiconf.Configuration([ ...loaders... ])
```
Configuration is being read at the moment of an object creation, all `get` are fast and read-only operations. Sources of the configuration are defined by loaders list, that will be described later.

You may also create multiple configurations with different sources - for example, parse command line parameters first, to define configuration files to be read as a full config later.

### Accessing parameters:

Configuration is treated as a tree of dicts and lists. For best compatibility, recommended to use only alphanumeric symbols and `_` as a key. Point `.` inside the key is treated as a divider between nested sections during both parsing ang getting.

After being parsed, tree could be received directly by `Configuration.as_dict()` method. 

Different parameters could be received via get operators: with auto cast (`config.get_bool(...)`, `config.get_int(...)`, etc) or by generic `get` method. `get` methods receive `key_path` parameter (e.g. `section_1.subsection.key_name`) and optional `default` parameter of any type, including `None`. `KeyError` will be raised, if key was not found and default option was not provided.

### Loaders:
Loaders are objects, that read configuration from different sources. Loaders are executed in direct order, later loaders will override previously parsed options with the same keys.

`JsonLoader` and `IniLoader` are both take optional `config_files_pattern` parameter, describing `glob` pattern to files with configuration. If not provided, parser will look for all `*.json/*.ini` files in the caller directory recursively.

`EnvLoader` takes optional `pattern` parameter, to define keys to be added in configuration.

`ArgsLoader` looks for all command line parameters with `key=value` format, with optional number of `-` as a prefix.

### Custom loaders:
If you want to write your own loader, you could simply inherit from `flexiconf.BaseLoader` class and implement `load` method.

### Contribution:
If you have some improvements, bug fixes or think, that your loader will be useful for other people, feel free to create pull request!