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
import importlib.resources
from pathlib import Path

from tools.htmls import Transform, unpack, create_div, create_element, create_label
from tools.htmls.utils import ListTransform
from tools.semantic import config
from tools.semantic.components import components
from tools.semantic.html_elements import *
from tools.semantic.layout import *

from tools.semantic import styles


class Semantic(ListTransform):
    static_semantic_root = Path(importlib.resources.path("tools.semantic", "static"))

    def __init__(self):
        super().__init__()

    def __transform__(self):
        return [
            create_element("link", rel="stylesheet",
                           href="/static/semantic/semantic" + (".min.css" if config.minified else ".css")),
            create_element("script", src="/static/semantic/semantic" + (".min.js" if config.minified else ".js")),
            *unpack([
                component.gather() for component in components.values()
            ]),
        ]
