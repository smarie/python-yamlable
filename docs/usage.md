# Usage

You have seen in the [main page](./index) a small example to understand the concepts. Below we present other advanced usages.

## `YamlCodec`

Sometimes you do not have the possibility to change the classes of the objects that you wish to encode/decode. In this case the solution is to write an independent codec, inheriting from `YamlCodec`. Once again this feature leverages the `multi_constructor` and `multi_representer` concepts available in the `PyYaml` internals, but with `YamlCodec` it becomes a bit easier to do.

Let's assume that the following two classes are given and can not be modified:

```python
class Foo:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return vars(self) == vars(other)

class Bar:
    def __init__(self, c):
        self.c = c

    def __eq__(self, other):
        return vars(self) == vars(other)
```

Writing a codec is quite simple:

 - first inherit from `YamlCodec` and fill `get_yaml_prefix` so that it returns the common prefix that all yaml objects encoded/decoded by this codec will use
 - then fill the checkers:
    - `get_known_types` to return all object types that can be encoded by this codec
    - `is_yaml_tag_supported` to return `True` if a yaml tag (suffix) is supported by this codec for decoding.
 - finally fill the encoder/decoder:
    - `from_yaml_dict` to decode
    - `to_yaml_dict` to encode

The example below shows how it can be done:


```python
from yamlable import YamlCodec
from typing import Type, Any, Iterable, Tuple


# the yaml tag suffixes for the two classes
foo_yaml = "yaml.tests.Foo"
bar_yaml = "yaml.tests.Bar"

# 2-way mappings between the types and the yaml tags
types_to_yaml_tags = {Foo: foo_yaml,
                      Bar: bar_yaml}
yaml_tags_to_types = {foo_yaml: Foo,
                      bar_yaml: Bar}

class MyCodec(YamlCodec):
    @classmethod
    def get_yaml_prefix(cls):
        return "!mycodec/"  # This is our root yaml tag

    # ---- 

    @classmethod
    def get_known_types(cls) -> Iterable[Type[Any]]:
        # return the list of types that we know how to encode
        return types_to_yaml_tags.keys()

    @classmethod
    def is_yaml_tag_supported(cls, yaml_tag_suffix: str) -> bool:
        # return True if the given yaml tag suffix is supported
        return yaml_tag_suffix in yaml_tags_to_types.keys()

    # ----

    @classmethod
    def from_yaml_dict(cls, yaml_tag_suffix: str, dct, **kwargs):
        # Create an object corresponding to the given tag, from the decoded dict
        typ = yaml_tags_to_types[yaml_tag_suffix]
        return typ(**dct)

    @classmethod
    def to_yaml_dict(cls, obj) -> Tuple[str, Any]:
        # Encode the given object and also return the tag that it should have
        return types_to_yaml_tags[type(obj)], vars(obj)
```

When you codec has been defined, it needs to be registerd before being usable. You can specify with which `PyYaml` Loaders/Dumpers it should be registered, or use the default (all): 

```python
# register the codec
MyCodec.register_with_pyyaml()
```

Finally let's test that the codec works:

```python
from yaml import dump, load

# instantiate
f = Foo(1, 'hello')
fy = "!mycodec/yaml.tests.Foo {a: 1, b: hello}\n"

b = Bar('what?')
by = "!mycodec/yaml.tests.Bar {c: 'what?'}\n"

# dump
assert dump(f) == fy
assert dump(b) == by

# load
assert f == load(fy)
assert b == load(by)
```
