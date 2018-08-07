# Changelog

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
