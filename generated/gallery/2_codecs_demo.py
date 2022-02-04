#  Authors: Sylvain MARIE <sylvain.marie@se.com>
#            + All contributors to <https://github.com/smarie/python-yamlable>
#
#  License: 3-clause BSD, <https://github.com/smarie/python-yamlable/blob/master/LICENSE>
"""
Writing Codecs
==============

Handle Yaml-ability for several classes at once, without modifying them.

What if you can not modify the class and still would like to make it yaml-able ? For such a (frequent) situation
`yamlable` provides another possibility: writing so-called "codecs".  A codec is a subclass of `YamlCodec` that will
handle several classes at once, typically classes that you cannot modify.


1. Writing a codec class
------------------------

Sometimes you do not have the possibility to change the classes of the objects that you wish to encode/decode.
In this case the solution is to write an independent codec, inheriting from `YamlCodec`. Once again this feature
leverages the `multi_constructor` and `multi_representer` concepts available in the `PyYaml` internals, but with
`YamlCodec` it becomes a bit easier to do.

Let's assume that the following two classes are given and can not be modified:

"""


class Foo:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __repr__(self):
        return f"{type(self).__name__} - {vars(self)}"

class Bar:
    def __init__(self, c):
        self.c = c

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __repr__(self):
        return f"{type(self).__name__} - {vars(self)}"

# %%
# Writing a codec is quite simple:
#
#  - first inherit from `YamlCodec` and fill `get_yaml_prefix` so that it returns the common prefix that all yaml
#    objects encoded/decoded by this codec will use
#  - then fill the checkers:
#     - `get_known_types` to return all object types that can be encoded by this codec
#     - `is_yaml_tag_supported` to return `True` if a yaml tag (suffix) is supported by this codec for decoding.
#  - finally fill the encoder/decoder:
#     - `from_yaml_dict` to decode. As opposed to the [single class example](), this method also receives the tag so
#       as to load the right object type.
#     - `to_yaml_dict` to encode. As opposed to the [single class example](), this method should return a tuple with
#       (yaml_tag, dict) so that different objects can be dumped as different yaml tags.
#
# The example below shows how it can be done:

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

# %%
# 2. Registering a codec
# ----------------------
#
# When you codec has been defined, it needs to be registered before being usable. You can specify with which `PyYaml`
# Loaders/Dumpers it should be registered, or use the default (all):

# register the codec
MyCodec.register_with_pyyaml()

# %%
# 3. Using a codec
# ----------------
#
# Finally let's test that the codec works:

from yaml import dump, safe_load

# instantiate
f = Foo(1, 'hello')
print(dump(f))

b = Bar('what?')
print(dump(b))

# %%

# load
fy = "!mycodec/yaml.tests.Foo {a: 1, b: hello}\n"
print(safe_load(fy))

by = "!mycodec/yaml.tests.Bar {c: 'what?'}\n"
print(safe_load(by))

# %%
# 4. Sequences and scalars
# ------------------------
#
# Objects can be loaded from sequences and scalars, in addition to dictionaries. To support this possibility, you
# simply need to fill the class methods:
#
#  - `from_yaml_list` for sequences
#  - `from_yaml_scalar` for scalars


class MyCodec2(MyCodec):
    @classmethod
    def from_yaml_list(cls, yaml_tag_suffix, seq, **kwargs):
        typ = yaml_tags_to_types[yaml_tag_suffix]
        return typ(*seq)

    @classmethod
    def from_yaml_scalar(cls, yaml_tag_suffix, scalar, **kwargs):
        typ = yaml_tags_to_types[yaml_tag_suffix]
        return typ(scalar)


# register the codec
MyCodec2.register_with_pyyaml()

# %%
# Then loading from sequence works

by_seq = """!mycodec/yaml.tests.Bar
- what?
"""
safe_load(by_seq)

# %%
# As well as scalar

by_scalar = "!mycodec/yaml.tests.Bar what?"
safe_load(by_scalar)
