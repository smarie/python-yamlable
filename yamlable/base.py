from abc import ABC, abstractmethod
from collections import OrderedDict
from io import TextIOBase, StringIO
from typing import Union, TypeVar, Dict, Any

try:
    from typing import Type
except ImportError:
    pass # normal for old versions of typing


Y = TypeVar('Y', bound='AbstractYamlObject')


class AbstractYamlObject(ABC):
    """
    Adds convenient methods load(s)_yaml/dump(s)_yaml to any object, to call pyyaml features directly on the object or
    on the object class.

    Also adds the two methods to_yaml_dict / from_yaml_dict, that are common to YamlObject2 and YamlAble.
    Default implementation uses vars(self) and cls(**dct), but subclasses can override.
    """

    def to_yaml_dict(self) -> Dict[str, Any]:
        """
        Implementors should transform the object into a dictionary containing all information necessary to decode the
        object in the future. That dictionary will be serialized as a YAML mapping.

        Default implementation returns vars(self). TODO maybe some day we'll need to rather make a copy...?
        :return:
        """
        return vars(self)

    @classmethod
    def from_yaml_dict(cls: 'Type[Y]', dct: Dict[Any, Any], yaml_tag: str) -> Y:
        """
        Implementors should transform the given dictionary (read from yaml by the pyYaml stack) into an object instance.
        The yaml tag associated to this object, read in the yaml document, is provided in parameter.

        Note that for YamlAble and YamlObject2 subclasses, if this method is called the yaml tag will already have
        been checked so implementors do not have to validate it.

        Default implementation returns cls(**dct)

        :param dct:
        :param yaml_tag: the yaml schema id that was used for encoding the object (it has already been checked
            against is_json_schema_id_supported)
        :return:
        """
        return cls(**dct)

    def dump_yaml(self, file_path_or_stream: Union[str, TextIOBase], safe: bool = True, **pyyaml_kwargs):
        """
        Dumps this object to a yaml file or stream using pyYaml.

        :param file_path_or_stream: either a string representing the file path, or a stream where to write
        :param safe: True (default) uses `yaml.safe_dump`. False uses `yaml.dump`
        :param pyyaml_kwargs: keyword arguments for the pyYaml dump method
        :return:
        """
        from yaml import safe_dump, dump
        if isinstance(file_path_or_stream, str):
            with open(file_path_or_stream, mode='wt') as f:
                if safe:
                    safe_dump(self, f, **pyyaml_kwargs)
                else:
                    dump(self, f, **pyyaml_kwargs)
        else:
            with file_path_or_stream as f:
                if safe:
                    safe_dump(self, f, **pyyaml_kwargs)
                else:
                    dump(self, f, **pyyaml_kwargs)

    def dumps_yaml(self, safe: bool = True, **pyyaml_kwargs):
        """
        Dumps this object to a yaml string and returns it.

        :param pyyaml_kwargs: keyword arguments for the pyYaml dump method
        :param safe: True (default) uses `yaml.safe_dump`. False uses `yaml.dump`
        :return:
        """
        from yaml import safe_dump, dump
        if safe:
            return safe_dump(self, **pyyaml_kwargs)
        else:
            return dump(self, **pyyaml_kwargs)

    @classmethod
    def loads_yaml(cls: 'Type[Y]', yaml_str: str, safe: bool=True) -> Y:
        """
        Utility method to load an instance of this class from the provided yaml string. This methods only returns
        successfully if the result is an instance of `cls`.

        :param yaml_str:
        :param safe: True (default) uses `yaml.safe_load`. False uses `yaml.load`
        :return:
        """
        return cls.load_yaml(StringIO(yaml_str), safe=safe)

    @classmethod
    def load_yaml(cls: 'Type[Y]', file_path_or_stream: Union[str, TextIOBase], safe: bool=True) -> Y:
        """
        Parses the given file path or stream as a yaml document. This methods only returns successfully if the result
        is an instance of `cls`.

        :param file_path_or_stream:
        :param safe: True (default) uses `yaml.safe_load`. False uses `yaml.load`
        :return:
        """
        from yaml import safe_load, load
        if isinstance(file_path_or_stream, str):
            with open(file_path_or_stream, mode='rt') as f:
                if safe:
                    res = safe_load(f.read())
                else:
                    res = load(f.read())
        else:
            with file_path_or_stream as f:
                if safe:
                    res = safe_load(f.read())
                else:
                    res = load(f.read())

        if isinstance(res, cls):
            return res
        else:
            raise TypeError("Decoded object is not an instance of {}, but a {}. Please make sure that the YAML document"
                            " starts with the tag defined in you class' `yaml_tag` field, for example `!my_type`"
                            "".format(cls.__name__, type(res).__name__))


NONE_IGNORE_CHECKS = object()
""" A tag to be used as yaml tag for abstract classes, to indicate that they are abstract (checks disabled) """


def read_yaml_node_as_dict(loader, node):
    """
    Utility method to read a yaml node into a dictionary

    :param loader:
    :param node:
    :return:
    """
    loader.flatten_mapping(node)
    pairs = loader.construct_pairs(node, deep=True)  # 'deep' allows the construction to be complete (inner seq...)
    constructor_args = OrderedDict(pairs)
    return constructor_args
