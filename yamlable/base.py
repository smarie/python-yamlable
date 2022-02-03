#  Authors: Sylvain MARIE <sylvain.marie@se.com>
#            + All contributors to <https://github.com/smarie/python-yamlable>
#
#  License: 3-clause BSD, <https://github.com/smarie/python-yamlable/blob/master/LICENSE>

from abc import ABCMeta
from collections import OrderedDict

from yaml import ScalarNode, SequenceNode, MappingNode

try:
    # Python 2 only:
    from StringIO import StringIO as _StringIO  # type: ignore  # noqa

    # create a variant that can serve as a context manager
    class StringIO(_StringIO):
        def __enter__(self):
            return self

        def __exit__(self, exception_type, exception_value, traceback):
            self.close()

except ImportError:
    # (IOBase is only used in type hints)
    from io import IOBase, StringIO  # type: ignore

from warnings import warn

import six

try:  # python 3.5+
    from typing import Union, TypeVar, Dict, Any, Sequence

    Y = TypeVar('Y', bound='AbstractYamlObject')

except ImportError:
    pass

try:  # python 3.5.4+
    from typing import Type
except ImportError:
    pass  # normal for old versions of typing


class AbstractYamlObject(six.with_metaclass(ABCMeta, object)):
    """
    Adds convenient methods load(s)_yaml/dump(s)_yaml to any object, to call pyyaml features directly on the object or
    on the object class.

    Also adds the two methods __to_yaml_dict__ / __from_yaml_dict__, that are common to YamlObject2 and YamlAble.
    Default implementation uses vars(self) and cls(**dct), but subclasses can override.
    """

    # def __to_yaml_scalar__(self):
    #     # type: (...) -> Any
    #     """
    #     Implementors should transform the object into a scalar containing all information necessary to decode the
    #     object as a YAML scalar in the future.
    #
    #     Default implementation raises an error.
    #     :return:
    #     """
    #     raise NotImplementedError("Please override `__to_yaml_scalar__` if you wish to dump instances of `%s`"
    #                               " as yaml scalars." % type(self).__name__)
    #
    # def __to_yaml_list__(self):
    #     # type: (...) -> Sequence[Any]
    #     """
    #     Implementors should transform the object into a Sequence containing all information necessary to decode the
    #     object as a YAML sequence in the future.
    #
    #     Default implementation raises an error.
    #     :return:
    #     """
    #     raise NotImplementedError("Please override `__to_yaml_list__` if you wish to dump instances of `%s`"
    #                               " as yaml sequences." % type(self).__name__)

    def __to_yaml_dict__(self):
        # type: (...) -> Dict[str, Any]
        """
        Implementors should transform the object into a dictionary containing all information necessary to decode the
        object in the future. That dictionary will be serialized as a YAML mapping.

        Default implementation returns vars(self).
        :return:
        """
        # Legacy compliance with old 'not dunder' method name TODO remove in future version
        if 'to_yaml_dict' in dir(self):
            warn(type(self).__name__ + " still uses the legacy method name 'to_yaml_dict'. This name will not be "
                                       "supported in future version, please use '__to_yaml_dict__' instead")
            return self.to_yaml_dict()  # type: ignore

        # Default: return vars(self) (Note: no need to make a copy, pyyaml does not modify it)
        return vars(self)

    @classmethod
    def __from_yaml_scalar__(cls,      # type: Type[Y]
                             scalar,   # type: Any
                             yaml_tag  # type: str
                             ):
        # type: (...) -> Y
        """
        Implementors should transform the given scalar (read from yaml by the pyYaml stack) into an object instance.
        The yaml tag associated to this object, read in the yaml document, is provided in parameter.

        Note that for YamlAble and YamlObject2 subclasses, if this method is called the yaml tag will already have
        been checked so implementors do not have to validate it.

        Default implementation returns cls(scalar)

        :param scalar: the yaml scalar
        :param yaml_tag: the yaml schema id that was used for encoding the object (it has already been checked
            against is_json_schema_id_supported)
        :return:
        """
        # Default: call constructor with positional arguments
        return cls(scalar)  # type: ignore

    @classmethod
    def __from_yaml_list__(cls,      # type: Type[Y]
                           seq,      # type: Sequence[Any]
                           yaml_tag  # type: str
                           ):
        # type: (...) -> Y
        """
        Implementors should transform the given Sequence (read from yaml by the pyYaml stack) into an object instance.
        The yaml tag associated to this object, read in the yaml document, is provided in parameter.

        Note that for YamlAble and YamlObject2 subclasses, if this method is called the yaml tag will already have
        been checked so implementors do not have to validate it.

        Default implementation returns cls(*seq)

        :param seq: the yaml sequence
        :param yaml_tag: the yaml schema id that was used for encoding the object (it has already been checked
            against is_json_schema_id_supported)
        :return:
        """
        # Default: call constructor with positional arguments
        return cls(*seq)  # type: ignore

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
            return cls.from_yaml_dict(dct, yaml_tag)  # type: ignore

        # Default: call constructor with all keyword arguments
        return cls(**dct)  # type: ignore

    def dump_yaml(self,
                  file_path_or_stream,  # type: Union[str, IOBase, StringIO]
                  safe=True,            # type: bool
                  **pyyaml_kwargs       # type: Any
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
            with open(file_path_or_stream, mode='w+t') as f:
                if safe:
                    safe_dump(self, f, **pyyaml_kwargs)
                else:
                    dump(self, f, **pyyaml_kwargs)
        else:
            with file_path_or_stream as f:  # type: ignore
                if safe:
                    safe_dump(self, f, **pyyaml_kwargs)
                else:
                    dump(self, f, **pyyaml_kwargs)

    def dumps_yaml(self,
                   safe=True,       # type: bool
                   **pyyaml_kwargs  # type: Any
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
            with file_path_or_stream as f:  # type: ignore
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


NONE_IGNORE_CHECKS = None
# """Tag to be used as yaml tag for abstract classes, to indicate that
# they are abstract (checks disabled). Not used anymore, kept for legacy reasons"""


def read_yaml_node_as_dict(loader, node):
    # type: (...) -> OrderedDict
    """
    Utility method to read a yaml node into a dictionary

    :param loader:
    :param node:
    :return:
    """
    # loader.flatten_mapping(node)
    # pairs = loader.construct_pairs(node, deep=True)  # 'deep' allows the construction to be complete (inner seq...)
    pairs = loader.construct_mapping(node, deep=True)  # 'deep' allows the construction to be complete (inner seq...)
    constructor_args = OrderedDict(pairs)
    return constructor_args


def read_yaml_node_as_sequence(loader, node):
    # type: (...) -> Sequence
    """
    Utility method to read a yaml node into a sequence

    :param loader:
    :param node:
    :return:
    """
    seq = loader.construct_sequence(node, deep=True)  # 'deep' allows the construction to be complete (inner seq...)
    return seq


def read_yaml_node_as_scalar(loader, node):
    # type: (...) -> Any
    """
    Utility method to read a yaml node into a sequence

    :param loader:
    :param node:
    :return:
    """
    value = loader.construct_scalar(node)
    return value


def read_yaml_node_as_yamlobject(
    cls,      # type: Type[AbstractYamlObject]
    loader,
    node,     # type: MappingNode
    yaml_tag  # type: str
):
    # type: (...) -> AbstractYamlObject
    """
    Default implementation: loads the node as a dictionary and calls __from_yaml_dict__ with this dictionary

    :param loader:
    :param node:
    :return:
    """
    if isinstance(node, ScalarNode):
        constructor_args = read_yaml_node_as_scalar(loader, node)
        return cls.__from_yaml_scalar__(constructor_args, yaml_tag=yaml_tag)  # type: ignore

    elif isinstance(node, SequenceNode):
        constructor_args = read_yaml_node_as_sequence(loader, node)
        return cls.__from_yaml_list__(constructor_args, yaml_tag=yaml_tag)  # type: ignore

    elif isinstance(node, MappingNode):
        constructor_args = read_yaml_node_as_dict(loader, node)
        return cls.__from_yaml_dict__(constructor_args, yaml_tag=yaml_tag)  # type: ignore

    else:
        raise TypeError("Unknown type of yaml node: %r. Please report this to `yamlable` project." % type(node))
