"""Copyright (C) 2024 Hadley Epstein

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, NamedTuple

from tools.htmls import Transform, TextBlock


# class Units(Enum):
#     def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
#         initial = ""
#         for c in name:
#             if c.isupper():
#                 initial+=c
#
#         return initial.lower()
#     MiliLiters = auto()
#     Liters = auto()
#     MiliGrams = auto()
#     Grams = auto()
#     KiloGrams = auto()
#
#     Pound = "lb"
#     Ounce = "ou"
#
#     Count = auto()
#     Pinch = auto()
#     Tin = auto()
#
#     None_ = auto()

class Abbrv(NamedTuple):
    abbrv: str
    format: str

class AbreviationEnum(Enum):
    def __new__(cls, *args):
        # print(cls)
        value: Abbrv

        obj = object.__new__(cls)
        # print(obj)

        arg0 = args[0]
        if type(arg0) == auto:
            arg0 = len(cls.__members__) + 1
        value = Abbrv(arg0, args[1])
        obj._value_ = value
        return obj


class Units(AbreviationEnum):
    Mililiters = "ml", "{name} {value} {abbrv}"
    Liters = "l", "{name} {value} {abbrv}"
    Miligrams = "mg", "{name} {value} {abbrv}"
    Grams = "g", "{name} {value} {abbrv}"
    Kilograms = "kg", "{name} {value} {abbrv}"

    Pound = "lb", "{name} {value} {abbrv}"
    Ounce = "ou", "{name} {value} {abbrv}"

    Count = auto(), None
    Pinch = auto(), None
    Tin = auto(), "{value} Tin of {name}"

    None_ = auto(), None


class TimeUnit(AbreviationEnum):
    Second = "s", "{value}{abbrv}"
    Hour = "hr", "{value}{abbrv}"
    Day = 'd', "{value}{abbrv}"


@dataclass
class Measure:
    value: any
    unit: Units

    def localise(self, name):
        if self.unit.name in ["Count", "None_", "Pinch"]:
            return None
        else:
            return self.unit.value.format.format(name=name, value=self.value, abbrv=self.unit.value.abbrv)


@dataclass
class Duration(Transform):
    duration: float
    unit: TimeUnit

    def __transform__(self):
        return TextBlock(self.unit.value.format.format(value=self.duration, abbrv=self.unit.value.abbrv))

    def __str__(self):
        return self.__transform__().elem_
