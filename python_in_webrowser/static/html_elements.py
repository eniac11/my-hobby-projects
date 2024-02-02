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

import tools
from tools import pyjack
from tools.event_system.event import Event
import tools.htmls.html
from tools.htmls import *
from js import document


@dataclass
class Events:
    click = Event()



class HTMLElement(Element):

    def __init__(self, name, *, styles: list["Style"] = None, inner: Element | str = None,
                 children: list[Element | str] = None,
                 single=False, class_=None, **kwargs):
        super().__init__(name, styles=styles, inner=inner,
                         children=children,
                         single=single, class_=class_, **kwargs)
        self._internal_elem = None

    def generate(self):
        elem = document.createElement(self.name)

        inner = self.inner
        # styles = ""
        # classes = equatify({'class': ' '.join(self.classes)})
        elem.classes = ' '.join(self.classes)

        if len(self.children) > 0:
            #     # inner += ''.join(map(str, map(transform, self.children)))
            for child in self.children:
                if issubclass(child.__class__, TextBlock):
                    child = transform(child)
                    text_node = document.createTextNode(child)
                    elem.appendChild(text_node)
                    continue

                child = transform(child)

                child.generate()
                elem.appendChild(child._internal_elem)
        #
        #     inner += self.transform_func(self.children)
        else:
            if self.inner is not None:
                inner = transform(inner)
                inner.generate()

        if len(self.styles) > 0:
            elem.styles = ''.join(map(str, self.styles))
            # styles = equatify({"style": ''.join(map(str, self.styles))})

        # kwargs = equatify(self._process_kwargs(self.kwargs))
        for key, val in self._process_kwargs(self.kwargs).items():
            elem.setAttribute(key, val)

        self._internal_elem = elem

    def display(self, output):
        self.generate()
        output.appendChild(self._internal_elem)

def setup():
    pyjack.replace_all_refs(Element_Constructor, HTMLElement)
