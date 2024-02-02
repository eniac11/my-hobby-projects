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
# Implements Custom element Classes
from __future__ import annotations
from typing import Type

import tools
from tools.htmls.html import Element


class NewElement(Element):
    def get_elements_by_type(self, cls: Type[NewElement]) -> list[NewElement]:
        elems = []
        if self.inner is not None:
            if isinstance(self.inner, cls):
                elems.append(self.inner)
            elif isinstance(self.inner, NewElement):
                elems.extend(self.inner.get_elements_by_type(cls))

        for child in self.children:
            if isinstance(child, cls):
                elems.append(child)
            elif isinstance(child, NewElement):
                elems.extend(child.get_elements_by_type(cls))

        return elems


tools.htmls.html.Element_Constructor = NewElement

from tools.htmls.html import BaseElement, Element, Element_Constructor


class Div(Element_Constructor):

    def __init__(self, **kwargs):
        super().__init__("div", **kwargs)


class Paragraph(Element_Constructor):

    def __init__(self, inner=None, **kwargs):
        super().__init__("p", inner=inner, **kwargs)


class ListElement(Element_Constructor):

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class OrderedListElement(ListElement):

    def __init__(self, **kwargs):
        super().__init__("ol", **kwargs)


class UnorderedListElement(ListElement):

    def __init__(self, **kwargs):
        super().__init__("ul", **kwargs)


class Header(Element_Constructor):

    def __init__(self, text, *, level=1, **kwargs):
        super().__init__("h" + str(level), inner=text, **kwargs)
        self._level = level

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if type(value) != int:
            raise TypeError("Header Level must be of time 'int'.")
        self._level = value
        self.name = "h" + str(self._level)


def default(value, or_):
    if value is None:
        return or_
    return value


class Image(Element_Constructor):

    def __init__(self, src, **kwargs):
        src = default(src, "")
        super().__init__("img", src=src, single=True, **kwargs)

    # @property
    def _getsrc(self):
        return self.kwargs["src"]

    # @src.setter
    def _setsrc(self, value: str):
        self.kwargs["src"] = value

    src = property(_getsrc, _setsrc, doc="""Image src attribute""")


class TableElement(Element_Constructor):

    def __init__(self, **kwargs):
        super().__init__("table", **kwargs)


class TableRowElement(Element_Constructor):

    def __init__(self, **kwargs):
        super().__init__("tr", **kwargs)


class TableDefinitionElement(Element_Constructor):

    def __init__(self, **kwargs):
        super().__init__("td", **kwargs)


class TableHeaderElement(Element_Constructor):

    def __init__(self, items: list[BaseElement], **kwargs):
        super().__init__("th", **kwargs)
        for item in items:
            self.add_child(TableDefinitionElement(inner=item))


class InputElement(Element_Constructor):

    def __init__(self, type_: str, name: str, /, id_=None, *, value=None, **kwargs):
        super().__init__("input", name_=name, type=type_, value=value, id=(name if id_ is None else id_),
                         **kwargs)
        self._type = type_

    @property
    def type(self):
        return self._type


class LabelElement(Element_Constructor):

    def __init__(self, for_: InputElement, label: str, **kwargs):
        super().__init__('label', for_=for_.get_id(), inner=label, **kwargs)


class ButtonInputElement(InputElement):

    def __init__(self, name: str, /, id_=None, *, value=None, **kwargs):
        super().__init__("button", name, id_, value=value, **kwargs)

class RadioInputElement(InputElement):
    def __init__(self, name, /, id_=None, *, value=None, **kwargs):
        super().__init__("radio", name, id_, value=value, **kwargs)


input_ = ButtonInputElement("hello")
label = LabelElement(input_, "This is a label")

document = Div(children=[
    Header("hello"),
    Paragraph("This is a paragraph"),
    label,
    input_,
    RadioInputElement("test", class_=["hello"])
])

from tools.htmls.styles import class_

c = class_("hello")

print(str(document))

print(document.get_elements_by_class_name(c()))
