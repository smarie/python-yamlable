# Changelog

### 1.1.0 - Now load objects from sequences and scalars too

 - Objects (subclasses of `YamlAble` or `YamlObject2`) can now be loaded from both mappings, sequences and scalars. Users may override the default behaviour by overriding `__from_yaml_list__` and `__from_yaml_scalar__`. Codecs (subclasses of `YamlCodec`) can also support this feature, through the `from_yaml_list` and `from_yaml_scalar` methods (not implemented by default). Fixes [#12](https://github.com/smarie/python-yamlable/issues/12)
 - Now using `mkdocs-gallery` for documentation examples. Fixed [#14](https://github.com/smarie/python-yamlable/issues/14)
 - `@yaml_info` can not be used on subclasses of `YamlObject2` anymore as it could lead to an unexpected behaviour. Fixes [#15](https://github.com/smarie/python-yamlable/issues/15)

### 1.0.4 - better type hinting (mypy)

 - Most type hints have been fixed, in particular for `@yaml_info`. Fixes [#11](https://github.com/smarie/python-yamlable/issues/11).
 - CI/CD pipeline migrated to Github Actions. Added badges using `genbadge`

### 1.0.3 - packaging improvements

 - packaging improvements: set the "universal wheel" flag to 1, and cleaned up the `setup.py`. In particular removed dependency to `six` for setup and added `py.typed` file, as well as set the `zip_safe` flag to False. Removed tests folder from package. Fixes [#10](https://github.com/smarie/python-yamlable/issues/10)

### 1.0.2 - `pyproject.toml`

Added `pyproject.toml`.

### 1.0.1 - added `__version__` attribute

Added `__version__` pkg-level attribute.

### 1.0.0 - Compliance with PyYaml 5.1 and de-facto 1.0.0

 * this version has been out and stable for long enough to be considered a good 1.0.0

 * PyYaml 5.1 added some breaking changes. We now comply with them while still supporting the old versions. Fixed [#8](https://github.com/smarie/python-yamlable/issues/8).

### 0.7.1 - minor fix

Fixed the file opening mode in `dump_yaml` method when a file path is provided as argument.

### 0.7.0 - Abstract class definition and checks have been simplified

It should now be easier to define an abstract yaml-able class for several object types.
Deprecated `NONE_IGNORE_CHECKS`. Fixes [#7](https://github.com/smarie/python-yamlable/issues/7)

### 0.6.0 - `YamlAble` does not provide a constructor anymore

Fixes [#6](https://github.com/smarie/python-yamlable/issues/6).

### 0.5.0 - Python 2.7 support

Fixes [#5](https://github.com/smarie/python-yamlable/issues/5)

### 0.4.0 - `YamlCodec` completed + dunder methods

`YamlCodec` completed (fixes [#4](https://github.com/smarie/python-yamlable/issues/4)):
 - `YamlCodec.decode_yamlable` renamed `decode` and `YamlCodec.encode_yamlable` renamed `encode`
 - added some checks in `YamlCodec.encode` to help users implement `to_yaml_dict` correctly
 - fixed bug in `register_with_pyyaml`: the wrong decoding method was registered
 - `YamlCodec.create_from_yaml_dict` renamed `from_yaml_dict` for consistency
 - added tests and usage documentation
 
Renamed internal `AbstractYamlObject` methods with dunder (fixes [#3](https://github.com/smarie/python-yamlable/issues/3)): 
 - `from_yaml_dict` becomes `__from_yaml_dict__` 
 - and `to_yaml_dict` become `__to_yaml_dict__`
Legacy names will remain supported for a while, added a tet to check that.


### 0.3.1 - minor error message improvement

 * Filled `yaml_info` docstring.
 * fixed class decoding so that it is robust to errors happening with faulty classes. This fixes [#2](https://github.com/smarie/python-yamlable/issues/2)
 * improved error message when decoding failed.

### 0.3.0 - safe parameter

 * Added the `safe` parameter to all dumping and loading methods `dump_yaml`, `dumps_yaml`, `load_yaml`, `loads_yaml`.

### 0.2.0 - Added default implementation

 * By default `to_yaml_dict` returns `vars(self)` and `from_yaml_dict` returns `cls(**dct)`. Fixes [#1](https://github.com/smarie/python-yamlable/issues/1)

### 0.1.0 - First public version

 * Initial fork from private repository
