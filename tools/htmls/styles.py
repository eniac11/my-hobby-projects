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

import copy
from enum import Enum, auto
from typing import Any, Optional

from tools.htmls.utils import Transform
from tools.htmls.html import Element_Constructor


class Style:

    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}: {self.value};"


class StyleType(Enum):
    CLASS = auto()
    ID = auto()
    STYLE = auto()


def convert_name(name, type_: StyleType, sub=False):
    if not sub:
        if type_ == StyleType.CLASS:
            return "." + name
        elif type_ == StyleType.ID:
            return "#" + name
    return name


class StyleDefinition:

    def __init__(self, name, type_: StyleType, sub=False):
        self.name = convert_name(name, type_, sub)
        self._defs = []
        self._styles = []
        self.type = type_
        self._current_style_def = self
        self._selector_stack = []
        self._selector_stack_editing = False

    @property
    def c(self):
        return self._current_style_def

    @c.setter
    def c(self, val):
        self._current_style_def = val

    def complete_selector_stack(self):
        if len(self._selector_stack) > 0:
            return self.c.name + ''.join(self.c._selector_stack)
        return self.name

    def pseudo(self, name) -> StyleDefinition:
        self.check_selector_stack_status()
        self._selector_stack.extend([":", name])
        return self

    def create_style_definition_if_needed(self, append=None):
        selector_stack = self.complete_selector_stack() + (append if append is not None else "")
        if selector_stack != self.c.name:
            style_def = StyleDefinition(selector_stack, self.type, True)
            self._defs.append(style_def)
            self._selector_stack_editing = False
            self.c = style_def
            self._selector_stack.clear()
            return True

        return False

    def check_selector_stack_status(self):
        if not self._selector_stack_editing:
            self._selector_stack.clear()
            self._selector_stack_editing = True

    def style(self, name, value) -> StyleDefinition:
        self.create_style_definition_if_needed()
        self.c._styles.append(Style(name, value))
        return self

    def child(self, name):
        self.check_selector_stack_status()
        self._selector_stack.extend([">", name])
        return self

    def select(self, name):
        self.check_selector_stack_status()
        self._selector_stack.extend([" ", name])
        return self

    def neighbour(self, name):
        self.check_selector_stack_status()
        self._selector_stack.extend(["+", name])
        return self

    def complete(self):
        if self.create_style_definition_if_needed():
            self.c = self
        self._selector_stack.clear()

        return self

    def change_name(self, new_name):
        for def_ in self._defs:
            def_.name = new_name + def_.name[len(self.name):]
        self.name = new_name

    def str_tag(self):
        if len(self._styles) > 0:
            return f"{self.name} {{ {''.join(map(str, self._styles))} }}"
        return ""

    def __call__(self, *args, **kwargs):
        return self.name[1:]

    def override(self):
        return StyleDefinition(self.name, self.type, True)

    def __str__(self):
        s = ""
        s += self.str_tag()
        for def_ in self._defs:
            s += str(def_)
        return s

    def styles(self, styles: list[Style]):
        self.create_style_definition_if_needed()
        self.c._styles.extend(styles)
        return self


class StyleContainer:
    current_container_context: StyleContainer = None

    def __init__(self):
        self.defs = []
        self.classes = []
        self.ids = []

    def add(self, style: StyleDefinition):
        if style.type == StyleType.CLASS:
            self.classes.append(style())
        if style.type == StyleType.ID:
            self.ids.append(style())
        style = copy.deepcopy(style)
        self.defs.append(style)

    def get_class(self, name):
        if name in self.classes:
            return name

    def __str__(self):
        s = ""
        s += ''.join(map(str, self.defs))
        return s

    def __enter__(self):
        StyleContainer.current_container_context = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        StyleContainer.current_container_context = None


class MediaQuery(StyleContainer):

    def __init__(self, query: str):
        super().__init__()
        self.query = query

    def __str__(self):
        s = super().__str__()
        s = f"@media {self.query} {{ {s} }}"
        return s


class StyleSheet(Transform):

    def __init__(self, body: StyleContainer, containers: list[StyleContainer] = None):
        super().__init__()
        self.style_body = body
        self.containers = containers
        if containers is None:
            self.containers = []
        self.containers.insert(0, body)

    def get_class(self, name):
        # print(name)
        for container in self.containers:
            if type(container) == StyleContainer:
                if (test := container.get_class(name)) is not None:
                    return test

    def __transform__(self):
        s = ""
        for container in self.containers:
            s += str(container)

        return Element_Constructor("style", inner=s)


def border_style(style='solid', width='5px'):
    return {'style': style, 'width': width}


def create_border(left: Optional[dict[str, str]] = None, right: Optional[dict[str, str]] = None,
                  top: Optional[dict[str, str]] = None, bottom: Optional[dict[str, str]] = None,
                  all: Optional[dict[str, str]] = None):
    styles = []
    if all is None:
        if left is not None:
            styles.append(Style('border-left', left['width']))
            styles.append(Style('border-left-style', left['style']))
        if right is not None:
            styles.append(Style('border-right', right['width']))
            styles.append(Style('border-right-style', right['style']))
        if top is not None:
            styles.append(Style('border-top', top['width']))
            styles.append(Style('border-top-style', top['style']))
        if bottom is not None:
            styles.append(Style('border-bottom', bottom['width']))
            styles.append(Style('border-bottom-style', bottom['style']))
    else:
        styles.append(Style('border', all['width']))
        styles.append(Style('border-style', all['style']))
    return styles


def style(name):
    def_ = StyleDefinition(name, StyleType.STYLE)
    StyleContainer.current_container_context.add(def_)
    return def_


def id_(name):
    def_ = StyleDefinition(name, StyleType.ID)
    StyleContainer.current_container_context.add(def_)
    return def_


def class_(name):
    def_ = StyleDefinition(name, StyleType.CLASS)
    StyleContainer.current_container_context.add(def_)
    return def_


body_style_container = StyleContainer()
