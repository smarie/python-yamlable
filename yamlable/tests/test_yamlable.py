from copy import copy
from typing import Dict, Any

import pytest
from yaml import dump, load

from yamlable import YamlAble, yaml_info, Y


def test_yamlable_incomplete_description():
    """ Tests that if __yaml_tag_suffix__ is not provided a YamlAble subclass cannot be declared """
    with pytest.raises(NotImplementedError) as err_info:
        class Foo(YamlAble):
            # __yaml_tag_suffix__ = 'foo'
            def to_yaml_dict(self) -> Dict[str, Any]:
                return copy(vars(self))

            @classmethod
            def from_yaml_dict(cls: 'Type[Y]', dct: Dict, yaml_tag: str) -> Y:
                return Foo(**dct)

        # instantiate
        f = Foo()

        # dump
        f.dumps_yaml()

    assert "does not seem to have a non-None '__yaml_tag_suffix__' field" in str(err_info.value)


def test_yamlable():
    """ Tests that YamlAbleMixIn works correctly """

    @yaml_info(yaml_tag_ns='yaml.tests')
    class Foo(YamlAble):
        # __yaml_tag_suffix__ = 'foo'   not needed: we used @yaml_info

        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __eq__(self, other):
            return vars(self) == vars(other)

        def to_yaml_dict(self) -> Dict[str, Any]:
            return copy(vars(self))

        @classmethod
        def from_yaml_dict(cls: 'Type[Y]', dct: Dict, yaml_tag: str) -> Y:
            return Foo(**dct)

    # instantiate
    f = Foo(1, 'hello')

    # dump
    y = f.dumps_yaml()
    assert y == "!yamlable/yaml.tests.Foo {a: 1, b: hello}\n"

    # dump pyyaml
    assert dump(f) == y

    # load
    assert f == Foo.loads_yaml(y)

    # load pyyaml
    assert f == load(y)


# TODO override so that tag is not supported, to check error message
def test_yamlable_not_supported():

    @yaml_info(yaml_tag_ns='yaml.tests')
    class Foo_Err(YamlAble):
        # __yaml_tag_suffix__ = 'foo'   not needed: we used @yaml_info

        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __eq__(self, other):
            return vars(self) == vars(other)

        def to_yaml_dict(self) -> Dict[str, Any]:
            return copy(vars(self))

        @classmethod
        def from_yaml_dict(cls: 'Type[Y]', dct: Dict, yaml_tag: str) -> Y:
            return Foo_Err(**dct)

        @classmethod
        def is_yaml_tag_supported(cls, yaml_tag: str):
            # ALWAYS return false
            return False

    with pytest.raises(TypeError) as err_info:
        Foo_Err.loads_yaml("!yamlable/yaml.tests.Foo_Err {a: 1, b: hello}\n")

    assert "No YamlAble subclass found able to decode object" in str(err_info.value)


def test_yamlable_default_impl():
    """ tests that the default implementation works """

    @yaml_info(yaml_tag_ns='yaml.tests')
    class Foo_Default(YamlAble):
        def __init__(self, a, b):
            self.a = a
            self.b = b

    f = Foo_Default(1, 'hello')
    s = '!yamlable/yaml.tests.Foo_Default {a: 1, b: hello}\n'
    assert dump(f) == s

    assert dump(load(dump(load(s)))) == s
