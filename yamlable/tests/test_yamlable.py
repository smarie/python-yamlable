from copy import copy
try:
    # Python 2 only:
    from StringIO import StringIO

    # create a variant that can serve as a context manager
    class StringIO(StringIO):
        def __enter__(self):
            return self
        def __exit__(self, exception_type, exception_value, traceback):
            self.close()

except ImportError:
    from io import StringIO

try: # python 3.5+
    from typing import Dict, Any
    from yamlable import Y
except ImportError:
    pass

import pytest
from yaml import dump, load

from yamlable import YamlAble, yaml_info


def test_yamlable_incomplete_description():
    """ Tests that if __yaml_tag_suffix__ is not provided a YamlAble subclass cannot be declared """
    with pytest.raises(NotImplementedError) as err_info:
        class Foo(YamlAble):
            # __yaml_tag_suffix__ = 'foo'
            def __to_yaml_dict__(self):
                # type: (...) -> Dict[str, Any]
                return copy(vars(self))

            @classmethod
            def __from_yaml_dict__(cls,  # type: Type[Y]
                                   dct,  # type: Dict[str, Any]
                                   yaml_tag  # type: str
                                   ):
                # type: (...) -> Y
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

        def __to_yaml_dict__(self):
            # type: (...) -> Dict[str, Any]
            return copy(vars(self))

        @classmethod
        def __from_yaml_dict__(cls,  # type: Type[Y]
                               dct,  # type: Dict[str, Any]
                               yaml_tag  # type: str
                               ):
            # type: (...) -> Y
            return Foo(**dct)

    # instantiate
    f = Foo(1, 'hello')  # note:

    # dump
    y = f.dumps_yaml()
    assert y == "!yamlable/yaml.tests.Foo {a: 1, b: hello}\n"

    # dump io
    class MemorizingStringIO(StringIO):
        """ A StringIO object that memorizes its buffer when it is closed (as opposed to the standard StringIO) """
        def close(self):
            self.value = self.getvalue()
            # super(StringIO, self).close()  # this does not work with python 2 old-style classes (StringIO is one)
            StringIO.close(self)

    s = MemorizingStringIO()
    f.dump_yaml(s)
    assert s.value == y

    # dump pyyaml
    assert dump(f) == y

    # load
    assert f == Foo.loads_yaml(y)

    # load io
    assert f == Foo.load_yaml(StringIO(y))

    # load pyyaml
    assert f == load(y)


def test_yamlable_legacy_method_names():
    """ Tests that YamlAbleMixIn works correctly """

    global enc
    global dec
    enc, dec = False, False

    @yaml_info(yaml_tag_ns='yaml.tests')
    class FooLegacy(YamlAble):
        # __yaml_tag_suffix__ = 'foo'   not needed: we used @yaml_info

        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __eq__(self, other):
            return vars(self) == vars(other)

        def to_yaml_dict(self):
            # type: (...) -> Dict[str, Any]
            global enc
            enc = True
            return copy(vars(self))

        @classmethod
        def from_yaml_dict(cls,  # type: Type[Y]
                               dct,  # type: Dict[str, Any]
                               yaml_tag  # type: str
                               ):
            # type: (...) -> Y
            global dec
            dec = True
            return FooLegacy(**dct)

    # instantiate
    f = FooLegacy(1, 'hello')

    # dump
    y = f.dumps_yaml()
    assert y == "!yamlable/yaml.tests.FooLegacy {a: 1, b: hello}\n"

    # dump io
    class MemorizingStringIO(StringIO):
        """ A StringIO object that memorizes its buffer when it is closed (as opposed to the standard StringIO) """
        def close(self):
            self.value = self.getvalue()
            # super(StringIO, self).close()  # this does not work with python 2 old-style classes (StringIO is one)
            StringIO.close(self)

    s = MemorizingStringIO()
    f.dump_yaml(s)
    assert s.value == y

    # dump pyyaml
    assert dump(f) == y

    # load
    assert f == FooLegacy.loads_yaml(y)

    # load io
    assert f == FooLegacy.load_yaml(StringIO(y))

    # load pyyaml
    assert f == load(y)

    assert enc
    assert dec


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

        def __to_yaml_dict__(self):
            # type: (...) -> Dict[str, Any]
            return copy(vars(self))

        @classmethod
        def __from_yaml_dict__(cls,  # type: Type[Y]
                               dct,  # type: Dict[str, Any]
                               yaml_tag  # type: str
                               ):
            # type: (...) -> Y
            return Foo_Err(**dct)

        @classmethod
        def is_yaml_tag_supported(cls,
                                  yaml_tag  # type: str
                                  ):
            # type: (...) -> bool
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


def test_help_yaml_info():

    @yaml_info("com.example.MyFoo")
    class Foo(YamlAble):
        pass

    assert Foo.__yaml_tag_suffix__ == "com.example.MyFoo"

    @yaml_info(yaml_tag_ns="com.example")
    class Foo(YamlAble):
        pass

    assert Foo.__yaml_tag_suffix__ == "com.example.Foo"

    assert Foo().dumps_yaml() == """!yamlable/com.example.Foo {}
"""
