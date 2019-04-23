from copy import copy
try:  # python 3.5+
    from typing import Dict, Any
    from yamlable import Y
except ImportError:
    pass

import pytest

from yamlable import YamlObject2


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

        def __to_yaml_dict__(self):
            # type: (...) -> Dict[str, Any]
            return copy(vars(self))

        @classmethod
        def __from_yaml_dict__(cls,      # type: Type[Y]
                               dct,      # type: Dict[str, Any]
                               yaml_tag  # type: str
                               ):
            # type: (...) -> Y
            return Foo(**dct)

    # instantiate
    f = Foo(1, 'hello')

    # dump to yaml
    o = f.dumps_yaml(safe=False, default_flow_style=False)
    assert o == """!foo
a: 1
b: hello
"""

    # load from yaml
    g = Foo.loads_yaml(o)
    assert f == g


def test_abstract_parent_error():
    """This tests that we can define an abstract parent class with the YamlAble behaviour and inherit it"""

    with pytest.raises(TypeError):
        class AbstractFooE(YamlObject2):
            pass

        # class FooError(AbstractFooE):
        #     """
        #     This class inherits from the parent without redefining a yaml tag
        #     """
        #     def __init__(self, a, b):
        #         self.a = a
        #         self.b = b
        #
        #     def __eq__(self, other):
        #         return vars(self) == vars(other)
        #
        # # instantiate
        # e = FooError(1, 'hello')
        #
        # # dump
        # with pytest.raises(NotImplementedError):
        #     e.dumps_yaml()


def test_abstract_parent():
    """This tests that we can define an abstract parent class with the YamlAble behaviour and inherit it"""

    class AbstractFooV(YamlObject2):
        # With YamlObject2 as opposed to YamlAble, we have to explicitly disable the yaml_tag field
        yaml_tag = None

    class FooValid(AbstractFooV):
        yaml_tag = '!foo'

        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __eq__(self, other):
            return vars(self) == vars(other)

    # instantiate
    f = FooValid(1, 'hello')

    # dump to yaml
    o = f.dumps_yaml(safe=False, default_flow_style=False)
    assert o == """!foo
a: 1
b: hello
"""

    # load from yaml
    g = FooValid.loads_yaml(o)
    assert f == g
