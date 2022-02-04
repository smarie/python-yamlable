# yamlable

*A thin wrapper of PyYaml to convert Python objects to YAML and back.*

[![Python versions](https://img.shields.io/pypi/pyversions/yamlable.svg)](https://pypi.python.org/pypi/yamlable/) [![Build Status](https://github.com/smarie/python-yamlable/actions/workflows/base.yml/badge.svg)](https://github.com/smarie/python-yamlable/actions/workflows/base.yml) [![Tests Status](./reports/junit/junit-badge.svg?dummy=8484744)](./reports/junit/report.html) [![Coverage Status](./reports/coverage/coverage-badge.svg?dummy=8484744)](./reports/coverage/index.html) [![Flake8 Status](./reports/flake8/flake8-badge.svg?dummy=8484744)](./reports/flake8/index.html)

[![Documentation](https://img.shields.io/badge/doc-latest-blue.svg)](https://smarie.github.io/python-yamlable/) [![PyPI](https://img.shields.io/pypi/v/yamlable.svg)](https://pypi.python.org/pypi/yamlable/) [![Downloads](https://pepy.tech/badge/yamlable)](https://pepy.tech/project/yamlable) [![Downloads per week](https://pepy.tech/badge/yamlable/week)](https://pepy.tech/project/yamlable) [![GitHub stars](https://img.shields.io/github/stars/smarie/python-yamlable.svg)](https://github.com/smarie/python-yamlable/stargazers) [![codecov](https://codecov.io/gh/smarie/python-yamlable/branch/main/graph/badge.svg)](https://codecov.io/gh/smarie/python-yamlable)

PyYaml is a great library. However it is a bit hard for anyone to add the yaml capability to their classes while keeping control on what's happening. Its `YamlObject` helper class is a first step but it has two drawbacks:

 * one has to master PyYaml Loader/Dumper internal features to understand what they are doing
 * there is a mandatory metaclass, which can prevent wide adoption (multiple inheritance with metaclasses...)

`yamlable` provides a very easy way for you to leverage PyYaml without seeing the complexity: simply inherit from `YamlAble`, decorate with `@yaml_info`, and you're set! 

You can then optionally override the methods `to_yaml_dict` and `from_yaml_dict` to write to / load from a dictionary, so as to adapt the yaml-ability to your class needs.

In addition `yamlable` provides a way to create Yaml codecs for several object types at the same time (`YamlCodec`) (see [Usage](./usage) page)


## Installing

```bash
> pip install yamlable
```

## Usage

See the [usage examples gallery](./generated/gallery).

## Main features / benefits

 * Add yaml-ability to any class easily through inheritance without metaclass (as opposed to `YamlObject`) and without knowledge of internal PyYaml loader/dumper logic.
 * Write codecs to support several types at a time and support classes that can't be modified, with `YamlCodec`
 * Supports loading from mappings, but also sequences and scalars. Dumping is always done as a mapping.
 * Alternate `YamlObject2` possibility, inheriting from pyyaml `YamlObject`.

## See Also

[PyYaml documentation](http://pyyaml.org/wiki/PyYAMLDocumentation)

### Others

*Do you like this library ? You might also like [my other python libraries](https://github.com/smarie/OVERVIEW#python)* 

## Want to contribute ?

Details on the github page: [https://github.com/smarie/python-yamlable](https://github.com/smarie/python-yamlable)
