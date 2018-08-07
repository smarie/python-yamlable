try:  # python 3.5+
    from typing import Tuple, Any, Iterable, Dict
except ImportError:
    pass

from yaml import dump, load

from yamlable import YamlCodec


def test_yamlcodec():
    """ Tests that custom yaml codec work """

    class Foo(object):
        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __eq__(self, other):
            return vars(self) == vars(other)

    class Bar(object):
        def __init__(self, c):
            self.c = c

        def __eq__(self, other):
            return vars(self) == vars(other)

    foo_yaml = "yaml.tests.Foo"
    bar_yaml = "yaml.tests.Bar"
    types_to_yaml_tags = {Foo: foo_yaml,
                          Bar: bar_yaml}
    yaml_tags_to_types = {foo_yaml: Foo,
                          bar_yaml: Bar}

    class MyCodec(YamlCodec):
        @classmethod
        def get_yaml_prefix(cls):
            return "!mycodec/"

        @classmethod
        def get_known_types(cls):
            # type: (...) -> Iterable[Type[Any]]
            return types_to_yaml_tags.keys()

        @classmethod
        def is_yaml_tag_supported(cls,
                                  yaml_tag_suffix  # type: str
                                  ):
            # type: (...) -> bool
            return yaml_tag_suffix in yaml_tags_to_types.keys()

        @classmethod
        def from_yaml_dict(cls,
                           yaml_tag_suffix,  # type: str
                           dct,              # type: Dict[str, Any]
                           **kwargs):
            # type: (...) -> Any
            typ = yaml_tags_to_types[yaml_tag_suffix]
            return typ(**dct)

        @classmethod
        def to_yaml_dict(cls, obj):
            # type: (...) -> Tuple[str, Any]
            return types_to_yaml_tags[type(obj)], vars(obj)

    # register the codec
    MyCodec.register_with_pyyaml()

    # instantiate
    f = Foo(1, 'hello')
    fy = "!mycodec/yaml.tests.Foo {a: 1, b: hello}\n"

    b = Bar('what?')
    by = "!mycodec/yaml.tests.Bar {c: 'what?'}\n"

    # dump pyyaml
    assert dump(f) == fy
    assert dump(b) == by

    # load pyyaml
    assert f == load(fy)
    assert b == load(by)
