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

from tools.web_framework import bottle
from tools.htmls import Transform, has_slot, set_slot, slot
from tools.htmls.html import *

from tools.htmls.html_elements import *
from typing import Any, Callable, Optional


class FormField(Transform):

    def __init__(self, type_: str, name: str, widget: Element_Constructor = None, default_value: Any = None,
                 required=False):
        input_elem = create_input(type_, name, value=default_value, required=required)
        widget = self.check_slot(widget, input_elem)
        super().__init__(widget)
        self.type_ = type_
        self.name = name
        self._value = default_value
        self.required = required
        self.elem_: Element_Constructor = self.elem_

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self.elem_.kwargs['value'] = val
        self._value = val

    def check_slot(self, widget, default=None):
        if widget is None:
            widget = default
        else:
            if has_slot(widget):
                set_slot(widget, default)
        return widget


class Form(Element_Constructor):
    def __init__(self, name: str, url: str, method: HTTPMethod, **kwargs):
        super().__init__('form', id=name, action=url, method=method, **kwargs)
        self._post: Optional[Callable[[Form], str]] = None
        self._get: Optional[Callable[[Form], str]] = None
        self.method = method
        self._url = url
        self.fields: list[FormField] = []
        self.filled = False

    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, val):
        self._url = val
        self.kwargs['action'] = val

    def add_field(self, field):
        self.fields.append(field)
        self.children.append(field)
        self.children.append(create_breakline())

    def get(self, func: Callable[[Form, Optional[list[Any]], Optional[dict[Any]]], str] = None, form: Form = None,
            *args, **kwargs):
        if func is None and self._get is not None:
            print(args)
            return self._get(form, *args, **kwargs)
        elif func is not None:
            self._get = func

    def post(self, func: Callable[[Form, Optional[list[Any]], Optional[dict[Any]]], str] = None, form: Form = None,
             *args, **kwargs):
        if func is None and self._get is not None:
            return self._post(form, *args, *kwargs)
        elif func is not None:
            self._post = func

    def __getitem__(self, name):
        for field in self.fields:
            if field.name == name:
                return field
        raise KeyError("No key: " + name)


class ComboboxField(FormField):

    def __init__(self, name: str, items: list[tuple[str, str]], default_index: int = 0, required=False, **kwargs):
        widget = create_element("select", children=[
            create_element('option', value=index, children=[name]) for index, name in items
        ], name_=name, required=required, **kwargs)
        super().__init__('combo', name, widget, required)

# class RadioField(FormField):
#
#     def __init__(self, name: str, items: list[tuple[str, str]], default_index: int = 0, required=False, **kwargs):


def create_input(type_, name, /, id_=None, *, value=None, **kwargs):
    return Element_Constructor("input", name_=name, type=type_, value=value, id=(name if id_ is None else id_),
                               **kwargs)


def create_label(for_: Element_Constructor, label: str, **kwargs):
    return Element_Constructor('label', for_=for_.get_id(), inner=label, **kwargs)


def labeled_elem(label, elem: Element_Constructor, *, reverse=False):
    if reverse:
        return create_div([elem, create_label(for_=elem, label=label)])
    return create_div([create_label(for_=elem, label=label), elem])


def create_radio(name, /, id_=None, *, value=None, **kwargs):
    return create_input('radio', name, id_, value=value, **kwargs)


def create_label_radio_group(label_, radios, *, new_line=False):
    for label, radio in radios:
        elem = create_radio(label_, id_=radio, value=label)
        lbl = labeled_elem(label, elem, reverse=True)
        yield lbl
        if new_line:
            yield [create_breakline()]
