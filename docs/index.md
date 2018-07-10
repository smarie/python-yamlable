# yamlable

*A thin wrapper of PyYaml to convert Python objects to YAML and back.*

[![Build Status](https://travis-ci.org/smarie/python-yamlable.svg?branch=master)](https://travis-ci.org/smarie/python-yamlable) [![Tests Status](https://smarie.github.io/python-yamlable/junit/junit-badge.svg?dummy=8484744)](https://smarie.github.io/python-yamlable/junit/report.html) [![codecov](https://codecov.io/gh/smarie/python-yamlable/branch/master/graph/badge.svg)](https://codecov.io/gh/smarie/python-yamlable) [![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://smarie.github.io/python-yamlable/) [![PyPI](https://img.shields.io/badge/PyPI-yamlable-blue.svg)](https://pypi.python.org/pypi/yamlable/)

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

Let's make a class yaml-able: we have to

 - inherit from `YamlAble`
 - decorate it with the `@yaml_info` annotation to declare the associated yaml tag
 - *optionally* implement `from_yaml_dict` (class method called during decoding) and/or `to_yaml_dict` (instance method called during encoding) if we wish to have control on the process, for example to only dump part of the attributes or perform some custom instance creation. Note that default implementation relies on `vars(self)` for dumping and on `cls(**dct)` for loading.
 
```python
from yamlable import yaml_info, YamlAble

@yaml_info(yaml_tag_ns='com.yamlable.example')
class Foo(YamlAble):

    def __init__(self, a, b):
        """ Constructor """
        self.a = a
        self.b = b
        self.irrelevant = 37

    def __str__(self):
        """ String representation for prints """
        return "Foo - " + str(dict(a=self.a, b=self.b))
    
    def to_yaml_dict(self):
        """ This optional method is called when you call yaml.dump()"""
        return {'a': self.a, 'b': self.b}

    @classmethod
    def from_yaml_dict(cls, dct, yaml_tag):
        """ This optional method is called when you call yaml.load()"""
        return Foo(dct['a'], dct['b'])
```

That's it! Let's check that our class is correct and allows us to create instances:

```python
>>> f = Foo(1, 'hello')
>>> print(f)

Foo - {'a': 1, 'b': 'hello'}
```

Now let's dump and load it using `pyyaml`:

```python
>>> import yaml
>>> print(yaml.dump(f))

!yamlable/com.yamlable.example.Foo {a: 1, b: hello}
```

```python
>>> print(yaml.safe_load("!yamlable/com.yamlable.example.Foo {a: 0, b: hey}"))

Foo - {'a': 0, 'b': 'hey'}
```

For more general cases where your object is embedded in a more complex structure for example, it will work as expected:

```python
>>> d = {'foo': f, 'foo2': 12}
>>> print(yaml.safe_dump(d))

foo: !yamlable/com.yamlable.example.Foo {a: 1, b: hello}
foo2: 12
```


In addition, the object directly offers the `dump_yaml` (dumping to file) / `dumps_yaml` (dumping to string) convenience methods, and the class directly offers the `load_yaml` (load from file) / `loads_yaml` (load from string) convenience methods.

See [PyYaml documentation](http://pyyaml.org/wiki/PyYAMLDocumentation) for the various formatting arguments that you can use, they are the same than in the `yaml.dump` method. For example:

```python
>>> print(f.dumps_yaml(default_flow_style=False))

!yamlable/com.yamlable.example.Foo
a: 1
b: hello
```

See [Usage](./usage) for other possibilities of `yamlable`.


## Main features / benefits

 * Add yaml-ability to any class easily through inheritance without metaclass (as opposed to `YamlObject`) and without knowledge of internal PyYaml loader/dumper logic.
 * Write codecs to support several types at a time with `YamlCodec`
 * If you absolutely wish to use PyYaml's `YamlObject` for some reason, you can use `YamlObject2` as an alternative to `YamlAble`. But it comes with the metaclass, like `YamlObject`.

## See Also

[PyYaml documentation](http://pyyaml.org/wiki/PyYAMLDocumentation)

### Others

*Do you like this library ? You might also like [my other python libraries](https://github.com/smarie/OVERVIEW#python)* 

## Want to contribute ?

Details on the github page: [https://github.com/smarie/python-yamlable](https://github.com/smarie/python-yamlable)
