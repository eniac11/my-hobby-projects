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
import copy
from typing import Type

from tools.htmls.forms import Form
from tools.htmls import *
from .bottle import BaseRequest, Request


def parse_form(form_constructor: Form, req: BaseRequest):
    copied_form = copy.copy(form_constructor)
    if copied_form.method == HTTPMethod.POST:
        for key, val in req.forms.items():
            copied_form[key].value = val
            copied_form.filled = True
    if copied_form.method == HTTPMethod.GET:
        for key, val in req.query.items():
            copied_form[key].value = val
            copied_form.filled = True

    return copied_form


class QueryField:

    def __init__(self, name):
        self.name = name
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, item):
        self._value = item

    def has_value(self):
        if self.value is not None:
            return True
        return False


class ListField(QueryField):

    def __init__(self, name):
        super().__init__(name)
        self.values = []

    @QueryField.value.setter
    def value(self, item):
        self.values.append(item)

    def has_value(self):
        return len(self.values) > 0


class EnumField(ListField):

    def __init__(self, name, enum_class: Type[Enum]):
        super().__init__(name)
        self.enum_class = enum_class

    @ListField.value.getter
    def value(self):
        return self._value

    @ListField.value.setter
    def value(self, item):
        if not self.has_value():
            self._value = self.enum_class[item.upper()]
        else:
            self._value |= self.enum_class[item.upper()]

    def has_value(self):
        if self.value is not None:
            return True
        return False


class ComparisonField(QueryField):

    def __init__(self, name, type_: Type):
        super().__init__(name)
        self.comparison = None
        self.type = type_

    @QueryField.value.setter
    def value(self, item):
        if item[0] in ["=", ">", "<"]:
            self.comparison = item[0]
        self._value = self.type(item[1:])

    def compare(self, other):
        match self.comparison:
            case "=":
                return self.value == other
            case ">":
                return other > self.value
            case "<":
                return other < self.value
        return False


class Query:

    def __init__(self, method: HTTPMethod = HTTPMethod.GET):
        self.fields: list[QueryField] = []
        self.method = method

    def __getitem__(self, item):
        for field in self.fields:
            if item == field.name:
                return field

    def add_field(self, field: QueryField):
        self.fields.append(field)


def parse_query(query_constructor: Query, req: Request):
    copied_query = copy.deepcopy(query_constructor)

    forms_dict = None
    if copied_query.method == HTTPMethod.POST and req.method == HTTPMethod.POST.value:
        forms_dict = req.forms
    if copied_query.method == HTTPMethod.GET and req.method == HTTPMethod.GET.value:
        forms_dict = req.query

    for field in copied_query.fields:
        if issubclass(field.__class__, ListField):
            for item in forms_dict.getall(field.name):
                if item is not None:
                    field.value = item
            continue
        if (test := forms_dict.get(field.name)) is not None:
            field.value = forms_dict.get(field.name)

    return copied_query
