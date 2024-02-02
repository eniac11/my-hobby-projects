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

import tools.markdown.markdown2 as markdown

from tools.htmls import Element, TextBlock


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


def _convert_str_html_to_htmls(source: str):
    source = "<dom>" + source + "</dom>"
    dom: xml.dom.minidom.Document = xml.dom.minidom.parseString(source)
    elem = _parse_element(dom.documentElement)
    return elem


def convert_markdown(source: str):
    return _convert_str_html_to_htmls(markdown.markdown(source, extras=["tables"])).children
