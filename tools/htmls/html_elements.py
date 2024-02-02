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
from .html import *


__all__ = ['create_div', 'create_breakline', 'create_element', 'create_button', 'create_image', 'create_p',
           'create_header', 'create_list_item', 'create_span']


def create_div(children, **kwargs):
    return Element_Constructor('div', children=children, **kwargs)


def create_breakline():
    return Element_Constructor('br', single=True)


# def create_form_label(inp: Element_Constructor, label: str,newline=False, children=None):
# label_elem = Element_Constructor('label', for_=inp.name, children=children)
# label_elem.inner = label
# if newline:
# return create_div(children=[label_elem, create_breakline(), inp])

# return create_div(children=[label_elem, inp])


def create_element(tag, /, inner=None, **kwargs):
    return Element_Constructor(tag, inner=inner, **kwargs)


def create_span(**kwargs):
    return create_element('span', **kwargs)


def create_p(inner=None, **kwargs):
    return create_element('p', inner, **kwargs)


def create_header(text, *, level=1, **kwargs):
    return create_element("h" + str(level), inner=text, **kwargs)


def create_image(src, **kwargs):
    return Element_Constructor('img', src=src, single=True, **kwargs)


def create_button(name, *, onclick=None, **kwargs):
    return Element_Constructor('button', inner=name, onclick=onclick, **kwargs)


def create_list_item(**kwargs):
    return Element_Constructor('li', **kwargs)
