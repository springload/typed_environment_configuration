# -*- coding: utf-8 -*-

from os import getenv
import typepy


def FillVars(variables, v, prefix=""):
    for var in variables:
        v[var.name] = var.getenv(prefix=prefix)


class Variable(object):
    _strict_level = 2  # for typepy

    def __init__(self, name, default=None, prefix=""):
        self._real_name = name
        self.default = default
        self.prefix = prefix

    def getenv(self, prefix=""):
        value = getenv(
            self._real_name, self.default if self.default is not None else None
        )
        if value is None:
            raise ValueError(
                "Please set required '{}' variable".format(self._real_name)
            )

        self.name = self._strip_prefix(self._real_name, self.prefix or prefix)

        try:
            return self._value_type(value, strict_level=self._strict_level).convert()
        except typepy._error.TypeConversionError:
            raise ValueError(
                "Can't convert variable '{}' with value '{}' to type '{}'".format(
                    self._real_name, value, repr(self._value_type)
                )
            )

    def _strip_prefix(self, name, prefix):
        if prefix and name.startswith(prefix):
            return name[len(prefix) :]
        else:
            return name


class EnvListConverter(typepy.converter.ListConverter):
    def force_convert(self):
        try:
            return list(
                (x.strip() for x in (self._value.split(",")) if x and x.strip())
            )
        except (TypeError, ValueError):
            raise TypeConversionError(
                "failed to force_convert to list: type={}".format(type(self._value))
            )


class StringEnvListVariable(typepy.type.List):
    def _create_type_checker(self):
        return typepy.checker.StringTypeChecker(self._data, self._strict_level)

    def _create_type_converter(self):
        return EnvListConverter(self._data)


class BoolVariable(Variable):
    _value_type = typepy.type.Bool
    _strict_level = 1


class StringVariable(Variable):
    _value_type = typepy.type.String
    _strict_level = 0


class StringListVariable(Variable):
    """
        Gets a string with vars separated by comma and turns them to list
    """

    _value_type = StringEnvListVariable
    _strict_level = 0
