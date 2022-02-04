#  Authors: Sylvain MARIE <sylvain.marie@se.com>
#            + All contributors to <https://github.com/smarie/python-yamlable>
#
#  License: 3-clause BSD, <https://github.com/smarie/python-yamlable/blob/master/LICENSE>
"""
Yaml-able classes
=================

Let's make a class yaml-aware so that instances can be loaded from YAML and dumped to
YAML.

1. Basics
---------

To make a class yaml-able, we have to

 - inherit from `YamlAble`
 - decorate it with the `@yaml_info` annotation to declare the associated yaml tag
"""

from yamlable import yaml_info, YamlAble

@yaml_info(yaml_tag_ns='com.yamlable.example')
class Foo(YamlAble):

    def __init__(self, a, b="hey"):
        """ Constructor """
        self.a = a
        self.b = b

    def __repr__(self):
        """ String representation for prints """
        return f"{type(self).__name__} - {dict(a=self.a, b=self.b)}"

# %%
# That's it! Let's check that our class is correct and allows us to create instances:

f = Foo(1, 'hello')
f


# %%
# Now let's dump it to a YAML document using `pyyaml`:

import yaml

print(yaml.dump(f))

# %%
# we can also load an instance from a document:

f2 = yaml.safe_load("""
!yamlable/com.yamlable.example.Foo
a: 0
b: hey
""")
print(f2)

# %%
# For more general cases where your object is embedded in a more complex structure for example, it will work as expected:

d = {'foo': f, 'foo2': 12}
print(yaml.dump(d))

# %%
# In addition, the object directly offers the `dump_yaml` (dumping to file) / `dumps_yaml` (dumping to string)
# convenience methods, and the class directly offers the `load_yaml` (load from file) / `loads_yaml` (load from string)
# convenience methods.
#
# See [PyYaml documentation](http://pyyaml.org/wiki/PyYAMLDocumentation) for the various formatting arguments that you
# can use, they are the same than in the `yaml.dump` method. For example:


print(f.dumps_yaml(default_flow_style=False))

# %%
# 2. Customization
# ----------------
#
# ### a. dumper/loader
#
# As could be seen above, `YamlAble` comes with a default implementation of the yaml formatting and parsing
# associated with the classes. This is controlled by two methods that you may wish to override:
#
#  - `__to_yaml_dict__` is an instance method that controls what to dump. By default it returns `vars(self)`
#  - `__from_yaml_dict__` is a class method that controls the loading process. By default it returns `cls(**dct)`.
#
# You may wish to override one, or both of these methods.
# For example if you do not wish to dump all of the object attributes:

@yaml_info(yaml_tag_ns='com.yamlable.example')
class CustomFoo(YamlAble):

    def __init__(self, a, b):
        """ Constructor """
        self.a = a
        self.b = b
        self.irrelevant = 37

    def __repr__(self):
        """ String representation for prints """
        return f"{type(self).__name__} - {dict(a=self.a, b=self.b, irrelevant=self.irrelevant)}"

    def __to_yaml_dict__(self):
        # Do not dump 'irrelevant'
        return {'a': self.a, 'b': self.b}

    @classmethod
    def __from_yaml_dict__(cls, dct, yaml_tag):
        # Accept a default value for b
        return cls(dct['a'], dct.get('b', "default"))

# %%
# Let's test it: loading...

f3 = yaml.safe_load("""
!yamlable/com.yamlable.example.CustomFoo
a: 0
""")
print(f3)

# %%
# ...and dumping again

print(f3.dumps_yaml())

# %%
# ### b. YAML tag
#
# You probably noticed in the above examples that the dumped YAML document contains a tag such as
# `!yamlable/com.yamlable.example.CustomFoo`.
#
# When you dump a `YamlAble` object `o` to yaml, the corresponding tag is `f!yamlable/{o.__yaml_tag_suffix__}`.
# Note that you can override the class attribute, or even the instance attribute:

f3.__yaml_tag_suffix__ = "wow_you_changed_me"
print(f3.dumps_yaml())

# %%
# The `@yaml_info` decorator is just a convenient way to fill the `__yaml_tag_suffix__` attribute on a class, nothing
# more.
# You can either provide a full yaml tag suffix:

@yaml_info("com.example.WowObject")
class MyFoo(YamlAble):
    pass

print(MyFoo.__yaml_tag_suffix__)
print(MyFoo().dumps_yaml())

# %%
# Notice that this is great for retrocompatiblity: you can change your class name or module without changing the
# YAML serialization.
#
# Otherwise you can simply provide a namespace, that will be appended with `.{cls.__name__}`:

@yaml_info(yaml_tag_ns="com.example")
class MyFoo(YamlAble):
    pass

print(MyFoo.__yaml_tag_suffix__)
print(MyFoo().dumps_yaml())

# %%
# In that case, you'll have to be sure that your class name does not change over time.
# If you do not like the `!yamlable` prefix, you should use the
# [alternate `YamlObject2` class](#3-alternate-way-yamlobject2) - in that case the decorator should not be used.
#
# 3. Alternate way: `YamlObject2`
# -------------------------------
# If you absolutely wish to use PyYaml's `YamlObject` for some reason, you can use `YamlObject2` as an alternative to
# `YamlAble`. But it comes with the metaclass, like `YamlObject`.
#
# Nevertheless, the way to work is very similar: simply override the optional methods. However you must specify the
# **entire** yaml tag directly using the `yaml_tag` class variable. The `@yaml_info` decorator
# can not be used with classes subclassing `YamlObject2`.

from yamlable import YamlObject2

class CustomFoo2(YamlObject2):
    yaml_tag = '!foo'

    def __init__(self, a, b):
        """ Constructor """
        self.a = a
        self.b = b
        self.irrelevant = 37

    def __repr__(self):
        """ String representation for prints """
        return f"{type(self).__name__} - {dict(a=self.a, b=self.b, irrelevant=self.irrelevant)}"

    def __to_yaml_dict__(self):
        # Do not dump 'irrelevant'
        return {'a': self.a, 'b': self.b}

    @classmethod
    def __from_yaml_dict__(cls, dct, yaml_tag):
        # Accept a default value for b
        return cls(dct['a'], dct.get('b', "default"))

# instantiate
f = CustomFoo2(1, 'hello')

# dump to yaml
o = yaml.dump(f)
print(o)

print(yaml.safe_load(o))


# %%
# 4. Support for sequences and scalars
# ------------------------------------
#
# Objects can also be loaded from YAML sequences:

yaml.safe_load("""
!yamlable/com.yamlable.example.Foo
- 0
- hey
""")

# %%
# The default implementation of `__from_yaml_list__` (that you may wish to override in your subclass), is to call
# the constructor with the sequence contents as positional arguments.
#
# The same also works for scalars:

yaml.safe_load("""
!yamlable/com.yamlable.example.Foo 0
""")

# %%
# The default implementation of `__from_yaml_scalar__` (that you may wish to override in your subclass), is to call
# the constructor with the scalar as first positional argument.
#
# !!! warning "Scalars are not resolved"
#     As can be seen in the above example, scalars are not auto-resolved when constructing an object from a scalar. So an
#     integer `0` is actually received as a string `"0"` by `from_yaml_scalar`.
