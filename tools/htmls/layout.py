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
from .utils import *
from .html_elements import *
from .styles import *

import copy


class Layout(Transform):

    def __init__(self):
        super().__init__()
        self.elem = None
        self.styles = None


def flex_item(child: Element_Constructor, grow=None):
    child = copy.deepcopy(child)
    child.styles.append(Style('flex', grow))
    return child


def flex(child: Element_Constructor, direction="row"):
    child = copy.deepcopy(child)
    child.styles.append(Style('display', 'flex'))
    child.styles.append(Style('flex-direction', direction))
    return child


def center(elem, **kwargs):
    return create_element('center', children=[elem], **kwargs)
