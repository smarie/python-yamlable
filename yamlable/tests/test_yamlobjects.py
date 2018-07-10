from copy import copy
from typing import Dict, Any

import pytest

from yamlable import YamlObject2, Y


def test_yamlobject_incomplete_description():
    """ Tests that if yaml_tag is not provided a YamlObject2 subclass cannot be declared """
    with pytest.raises(TypeError) as err_info:
        class Foo(YamlObject2):
            # yaml_tag = '!foo'
            pass

    assert str(err_info.value).startswith("`yaml_tag`")


def test_yamlobject_simple():
    """ Simple YamlObject2 test """

    class Foo(YamlObject2):
        yaml_tag = '!foo'

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

    # dump to yaml
    o = f.dumps_yaml(safe=False)
    assert o == "!foo {a: 1, b: hello}\n"

    # load from yaml
    g = Foo.loads_yaml(o)
    assert f == g
