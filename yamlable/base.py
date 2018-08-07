from abc import ABCMeta
from collections import OrderedDict

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
    # (IOBase is only used in type hints)
    from io import IOBase, StringIO

from warnings import warn

import six

try:  # python 3.5+
    from typing import Union, TypeVar, Dict, Any

    Y = TypeVar('Y', bound='AbstractYamlObject')

except ImportError:
    pass

try:  # python 3.5.4+
    from typing import Type
except ImportError:
    pass # normal for old versions of typing


class AbstractYamlObject(six.with_metaclass(ABCMeta, object)):
    """
    Adds convenient methods load(s)_yaml/dump(s)_yaml to any object, to call pyyaml features directly on the object or
    on the object class.

    Also adds the two methods __to_yaml_dict__ / __from_yaml_dict__, that are common to YamlObject2 and YamlAble.
    Default implementation uses vars(self) and cls(**dct), but subclasses can override.
    """

    def __to_yaml_dict__(self):
        # type: (...) -> Dict[str, Any]
        """
        Implementors should transform the object into a dictionary containing all information necessary to decode the
        object in the future. That dictionary will be serialized as a YAML mapping.

        Default implementation returns vars(self). TODO maybe some day we'll need to rather make a copy...?
        :return:
        """
        # Legacy compliance with old 'not dunder' method name TODO remove in future version
        if 'to_yaml_dict' in dir(self):
            warn(type(self).__name__ + " still uses the legacy method name 'to_yaml_dict'. This name will not be "
                                       "supported in future version, please use '__to_yaml_dict__' instead")
            return self.to_yaml_dict()

        # Default: return vars
        return vars(self)

    @classmethod
    def __from_yaml_dict__(cls,      # type: Type[Y]
                           dct,      # type: Dict[str, Any]
                           yaml_tag  # type: str
                           ):
        # type: (...) -> Y
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
        # Legacy compliance with old 'not dunder' method name TODO remove in future version
        if 'from_yaml_dict' in dir(cls):
            warn(cls.__name__ + " still uses the legacy method name 'from_yaml_dict'. This name will not be "
                                "supported in future version, please use '__from_yaml_dict__' instead")
            return cls.from_yaml_dict(dct, yaml_tag)

        # Default: call constructor with all keyword arguments
        return cls(**dct)

    def dump_yaml(self,
                  file_path_or_stream,  # type: Union[str, IOBase, StrinIO]
                  safe=True,            # type: bool
                  **pyyaml_kwargs       # type: Dict[str, Any]
                  ):
        # type: (...) -> None
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

    def dumps_yaml(self,
                   safe=True,       # type: bool
                   **pyyaml_kwargs  # type: Dict[str, Any]
                   ):
        # type: (...) -> str
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
    def loads_yaml(cls,          # type: Type[Y]
                   yaml_str,     # type: str
                   safe=True     # type: bool
                   ):
        # type: (...) -> Y
        """
        Utility method to load an instance of this class from the provided yaml string. This methods only returns
        successfully if the result is an instance of `cls`.

        :param yaml_str:
        :param safe: True (default) uses `yaml.safe_load`. False uses `yaml.load`
        :return:
        """
        return cls.load_yaml(StringIO(yaml_str), safe=safe)

    @classmethod
    def load_yaml(cls,                  # type: Type[Y]
                  file_path_or_stream,  # type: Union[str, IOBase, StringIO]
                  safe=True             # type: bool
                  ):
        # type: (...) -> Y
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
