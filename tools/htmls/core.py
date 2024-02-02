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
import xml.dom.minidom
from typing import Optional

from tools.htmls import base_style
from tools.htmls.html import *
# from tools.htmls.styles import StyleDef
from tools.htmls.utils import *
from tools.htmls.html_elements import *

__all__ = ['create_text', 'create_link', 'InternalLink',
           'Page', 'Link']


def create_link(url, /, inner=None, *, children=None, **kwargs):
    return Element_Constructor('a', inner=inner, href=url, children=children, **kwargs)


def create_text(inner):
    return Element_Constructor("span", inner=inner)


class Link(Transform):
    def __init__(self, url, text, external=False):
        self.url = url
        if external:
            self.url = "https://" + self.url
        self.text = text
        super().__init__(create_link(self.url, self.text))


class InternalLink(Transform):

    def __init__(self, linked_elem: Element_Constructor):
        self.url = "#" + linked_elem.get_id()
        super().__init__(create_link(self.url, inner=linked_elem, class_=base_style.internal_link()))
        self.internal_elem = linked_elem

    def link(self, /, inner=None, *, children=None):
        return create_link(self.url, inner=inner, children=children)


class Page:

    def __init__(self, *, head=None, body=None, onload=None):

        if head is None:
            head = []
        if body is None:
            body = []
        self.head = create_element('head', children=head)
        self.body = create_element('body', children=body, onload=onload)

    def __str__(self):
        return f"""<!DOCTYPE html>{create_element('html', children=[self.head, self.body])}"""



def _parse_children(element: xml.dom.minidom.Element):
    children = []
    for child in element.childNodes:
        children.append(_parse_element(child))
    return children


def _parse_element(element: xml.dom.minidom.Element):
    children = _parse_children(element)
    if type(element) == xml.dom.minidom.Text:
        element: xml.dom.minidom.Text
        return TextBlock(element.data)
    return Element(element.tagName, children=children)


def convert_str_html_to_htmls(source: str):
    source = "<dom>" + source + "</dom>"
    dom: xml.dom.minidom.Document = xml.dom.minidom.parseString(source)
    elem = _parse_element(dom.documentElement)
    return elem