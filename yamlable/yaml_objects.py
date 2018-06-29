from abc import ABCMeta
from typing import TypeVar
try:
    from typing import Type
except ImportError:
    pass # normal for old versions of typing
from yaml import YAMLObjectMetaclass, YAMLObject, SafeLoader

from yamlable.base import NONE_IGNORE_CHECKS, AbstractYamlObject, read_yaml_node_as_dict


YO2 = TypeVar('YO2', bound='YamlObject2')


class YAMLObjectMetaclassStrict(YAMLObjectMetaclass):
    """
    Improved metaclass for YAMLObject, that raises an error if yaml_tag is not defined
    """
    def __init__(cls: 'Type[YO2]', name, bases, kwds):

        # construct as usual
        super(YAMLObjectMetaclass, cls).__init__(name, bases, kwds)

        # if yaml_tag is provided
        if 'yaml_tag' in kwds and kwds['yaml_tag'] is not None:
            if cls.yaml_tag != NONE_IGNORE_CHECKS:
                cls.yaml_loader.add_constructor(cls.yaml_tag, cls.from_yaml)
                cls.yaml_dumper.add_representer(cls, cls.to_yaml)
            else:
                if 'yaml_tag' in cls.__dict__:
                    # this is an explicitly disabled class (yaml_tag=NONE_IGNORE_CHECK is set on it), ok
                    pass
                else:
                    # this class inherits from the yaml_tag=NONE_IGNORE_CHECK and does not redefine it, not ok
                    raise TypeError("`yaml_tag` field is not redefined by class {}, cannot inherit from YAMLObject "
                                    "properly. Note that abstract classes can use the tag NONE_IGNORE_CHECKS to skip "
                                    "this check. It won't disable the check for their subclasses".format(cls))

        else:
            raise TypeError("`yaml_tag` field is not redefined by class {}, cannot inherit from YAMLObject properly"
                            "".format(cls))


class ABCYAMLMeta(YAMLObjectMetaclassStrict, ABCMeta):
    """The subclass of both YAMLObjectMetaclass and ABCMeta, to be used in YamlObject2"""
    pass


class YamlObject2(AbstractYamlObject, YAMLObject, metaclass=ABCYAMLMeta):
    """
    A helper class to register a class as able to dump instances to yaml and to load them back from yaml.

    This class relies on the `YAMLObject` class provided in pyyaml, and implements the to_yaml/from_yaml methods by
    leveraging the VarsExposer/BuildableFromVars mix-ins.

    It is basically an extension of YAMLObject
     - mapping the methods to methods in AbstractYamlObject (for consistency with YamlAble) so that you only have to
     provide a mapping to dictionary and do not have to care about pyyaml internals
     - and raising an error if the `yaml_tag` class field is not properly set.

    You still have to
     - define `yaml_tag` either directly or using the @yaml_info() decorator
     - implement both methods from AbstractYamlObject: to_yaml_dict and from_yaml_dict

    Note: since this class extends YAMLObject, it relies on metaclass. You might therefore prefer to extend YamlAble
    instead.
    """
    yaml_loader = SafeLoader  # explicitly use SafeLoader by default
    # yaml_dumper = Dumper
    yaml_tag = NONE_IGNORE_CHECKS
    # yaml_flow_style = ...

    @classmethod
    def to_yaml(cls, dumper, data: AbstractYamlObject):
        """
        Default implementation: relies on AbstractYamlObject API to serialize all public variables

        :param dumper:
        :param data:
        :return:
        """
        new_data = data.to_yaml_dict()
        return dumper.represent_mapping(cls.yaml_tag, new_data, flow_style=cls.yaml_flow_style)

    @classmethod
    def from_yaml(cls, loader, node):
        """
        Default implementation: loads the node as a dictionary and calls from_yaml_dict with this dictionary

        :param loader:
        :param node:
        :return:
        """
        constructor_args = read_yaml_node_as_dict(loader, node)
        return cls.from_yaml_dict(constructor_args, yaml_tag=cls.yaml_tag)
