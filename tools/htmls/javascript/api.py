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
from .javascript import *

__all__ = ['console', 'JSON', 'fetch', 'document']

from .. import HTTPMethod

console = MappedClass('console', ['log'])
JSON = MappedClass('JSON', ['stringify'])
document = MappedClass('document', ['getElementById'])

_fetch = Function('fetch', ['url', 'data'], [])


def single_quote(string):
    return "'" + string + "'"


def js_dict(**kwargs):
    s = "{"
    for key, value in kwargs.items():
        s += single_quote(key) + ":"
        if type(value) == FunctionCall:
            value: FunctionCall


def fetch(url, method: HTTPMethod, type_: ContentTypes, data):
    data = {'method': method.value, 'headers': {'Content-Type': type_.value},
            'body': JSON.stringify([data]).call(True).code}

    return _fetch([single_quote(url), data], True)
