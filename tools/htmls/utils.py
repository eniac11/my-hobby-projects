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
from __future__ import annotations
import itertools
import uuid
import xml.dom
from typing import Any

__all__ = ['equatify', 'unpack', 'Transform', 'TextBlock', 'DelayedTransform', 'transform_block_to_text_block',
           'transform', 'process_variable_underscore']


def process_variable_underscore(val: str):
    val = val.strip("_")
    return val.replace("_", "-")


def equatify(d):
    s = ""
    for key, val in d.items():
        if type(val) == bool:
            if val:
                s += process_variable_underscore(key) + " "
        else:
            if val is not None:
                if type(val) == str and len(val) == 0:
                    continue
                s += f'{process_variable_underscore(key)}="{val}" '
    return s[:-1]


def unpack(iterable):
    return list(itertools.chain.from_iterable(iterable))


class Transform:
    def __init__(self, elem=None):
        self.elem_ = elem

    def __transform__(self):
        return self.elem_

    def replace(self, replacement):
        self.__dict__ = replacement.__dict__


class ListTransform(Transform):
    pass


class TextBlock(Transform):

    def __init__(self, text: str):
        super().__init__(text)
        self.id = uuid.uuid4()
        self.elem_: str = self.elem_


def transform_block_to_text_block(values: list[Any] | str):
    if type(values) == TextBlock:
        return values
    if type(values) == str:
        return TextBlock(values)

    if type(values) == list:
        for i, value in enumerate(values):
            if type(value) == str:
                values[i] = TextBlock(value)
    if type(values) == tuple:
        values = tuple(map(TextBlock, values))
    return values


class DelayedTransform(Transform):

    def __init__(self, elem, func):
        super().__init__(elem)
        self.func = func

    def __transform__(self):
        system = transform(self.elem_)
        # print("s", system)
        return self.func(system)


def transform(transformer):
    # print("f", transformer, type(transformer))
    if isinstance(transformer, Transform):

        attr = getattr(transformer, '__transform__')
        # if type(transformer) == TextBlock:
        #     print(transformer.elem, attr, attr())

        if (test := attr()) is None:
            return ''
        return transform(test)
    return transformer

