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
from tools.htmls import create_div, Element
from tools.semantic.html_elements import ui


def button_group(children=None, **kwargs):
    elem = ui(children=children, **kwargs)
    elem.classes.append("buttons")
    return elem


def column(elem: Element, ):
    elem.classes.append("column")
    return elem


def stackable(elem: Element):
    elem.classes.append("stackable")
    return elem


def grid(elem: Element, *, width="equal"):
    # elem.classes.append("width")
    elem.classes.append("grid")
    return elem
