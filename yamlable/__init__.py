#  Authors: Sylvain MARIE <sylvain.marie@se.com>
#            + All contributors to <https://github.com/smarie/python-yamlable>
#
#  License: 3-clause BSD, <https://github.com/smarie/python-yamlable/blob/master/LICENSE>

from yamlable.base import AbstractYamlObject, NONE_IGNORE_CHECKS, read_yaml_node_as_dict
from yamlable.main import YamlCodec, register_yamlable_codec, yaml_info_decorate, yaml_info, YamlAble, \
    AbstractYamlAble, YAMLABLE_PREFIX
from yamlable.yaml_objects import YamlObject2, ABCYAMLMeta, YAMLObjectMetaclassStrict

try:
    # -- Distribution mode --
    # import from _version.py generated by setuptools_scm during release
    from ._version import version as __version__
except ImportError:
    # -- Source mode --
    # use setuptools_scm to get the current version from src using git
    from setuptools_scm import get_version as _gv
    from os import path as _path
    __version__ = _gv(_path.join(_path.dirname(__file__), _path.pardir))

__all__ = [
    '__version__',
    # submodules
    'base', 'main', 'yaml_objects',
    # symbols
    'AbstractYamlObject', 'NONE_IGNORE_CHECKS', 'read_yaml_node_as_dict',
    'YamlCodec', 'register_yamlable_codec', 'yaml_info_decorate', 'yaml_info', 'YamlAble', 'AbstractYamlAble',
    'YAMLABLE_PREFIX',
    'YamlObject2', 'ABCYAMLMeta', 'YAMLObjectMetaclassStrict'
]

try:  # python 3.5+
    from yamlable.base import Y  # noqa: F401
    __all__.append('Y')
except ImportError:
    pass

try:  # python 3.5+
    from yamlable.main import YA  # noqa: F401
    __all__.append('YA')
except ImportError:
    pass
