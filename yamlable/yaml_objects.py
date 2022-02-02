#  Authors: Sylvain MARIE <sylvain.marie@se.com>
#            + All contributors to <https://github.com/smarie/python-yamlable>
#
#  License: 3-clause BSD, <https://github.com/smarie/python-yamlable/blob/master/LICENSE>

from abc import ABCMeta

import six

try:  # python 3.5+
    from typing import TypeVar

    YO2 = TypeVar('YO2', bound='YamlObject2')
except ImportError:
    pass
try:  # python 3.5.4+
    from typing import Type
except ImportError:
    pass  # normal for old versions of typing

from yaml import YAMLObjectMetaclass, YAMLObject, SafeLoader, MappingNode

from yamlable.base import AbstractYamlObject, read_yaml_node_as_yamlobject


class YAMLObjectMetaclassStrict(YAMLObjectMetaclass):
    """
    Improved metaclass for YAMLObject, that raises an error if yaml_tag is not defined
    """
    def __init__(cls,   # type: Type[YO2]  # type: ignore
                 name, bases, kwds):

        # construct as usual
        super(YAMLObjectMetaclass, cls).__init__(name, bases, kwds)

        # if yaml_tag is provided
        if 'yaml_tag' in kwds:
            # if cls.yaml_tag != NONE_IGNORE_CHECKS:
            if kwds['yaml_tag'] is not None:
                cls.yaml_loader.add_constructor(cls.yaml_tag, cls.from_yaml)
                cls.yaml_dumper.add_representer(cls, cls.to_yaml)
            else:
                if 'yaml_tag' in cls.__dict__:
                    # this is an explicitly disabled class (yaml_tag=None is set on it), ok
                    pass
                else:
                    # this class inherits from the yaml_tag=None and does not redefine it, not ok
                    raise TypeError("`yaml_tag` field is not redefined by class {}, cannot inherit from YAMLObject "
                                    "properly. Note that abstract classes can set the tag explicitly to `None` to skip "
                                    "this check. It won't disable the check for their subclasses".format(cls))

        else:
            raise TypeError("`yaml_tag` field is not redefined by class {}, cannot inherit from YAMLObject properly"
                            "".format(cls))


class ABCYAMLMeta(YAMLObjectMetaclassStrict, ABCMeta):
    """The subclass of both YAMLObjectMetaclass and ABCMeta, to be used in YamlObject2"""
    pass


class YamlObject2(six.with_metaclass(ABCYAMLMeta, AbstractYamlObject, YAMLObject)):
    """
    A helper class to register a class as able to dump instances to yaml and to load them back from yaml.

    This class relies on the `YAMLObject` class provided in pyyaml, and implements the to_yaml/from_yaml methods by
    leveraging the AbstractYamlObject class (__to_yaml_dict__ / __from_yaml_dict__).

    It is basically an extension of YAMLObject
     - mapping the methods to methods in AbstractYamlObject (for consistency with YamlAble) so that you only have to
     provide a mapping to dictionary and do not have to care about pyyaml internals
     - and raising an error if the `yaml_tag` class field is not properly set.

    You still have to
     - define `yaml_tag` either directly or using the @yaml_info() decorator
     - optionally override methods from AbstractYamlObject: __to_yaml_dict__ and __from_yaml_dict__

    Note: since this class extends YAMLObject, it relies on metaclass. You might therefore prefer to extend YamlAble
    instead.
    """
    yaml_loader = SafeLoader  # explicitly use SafeLoader by default
    # yaml_dumper = Dumper
    yaml_tag = None
    # yaml_flow_style = ...

    @classmethod
    def to_yaml(cls,    # type: Type[YamlObject2]
                dumper,
                data    # type: AbstractYamlObject
                ):
        # type: (...) -> MappingNode
        """
        Default implementation: relies on AbstractYamlObject API to serialize all public variables

        :param dumper:
        :param data:
        :return:
        """
        new_data = data.__to_yaml_dict__()
        return dumper.represent_mapping(cls.yaml_tag, new_data, flow_style=cls.yaml_flow_style)

    @classmethod
    def from_yaml(cls,   # type: Type[YamlObject2]
                  loader,
                  node   # type: MappingNode
                  ):
        # type: (...) -> YamlObject2
        """
        Default implementation: relies on AbstractYamlObject API to load the node as a dictionary/sequence/scalar

        :param loader:
        :param node:
        :return:
        """
        return read_yaml_node_as_yamlobject(cls=cls, loader=loader, node=node, yaml_tag=cls.yaml_tag)
