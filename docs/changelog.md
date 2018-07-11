# Changelog

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
