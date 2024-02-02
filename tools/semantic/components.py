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

from tools.htmls import create_script, create_element
from tools.semantic import config

extra_js = {"dropdown": """$(document)
    .ready(function() {
      $('.ui.dropdown').dropdown();

      $('.ui.buttons .dropdown.button').dropdown({
        action: 'combo'
      });
    })
  ;""",
            "menu": """$(document)
    .ready(function() {
      $('.ui.menu a.item')
        .on('click', function() {
          $(this)
            .addClass('active')
            .siblings()
            .removeClass('active')
          ;
        })
      ;
    })
  ;"""}


class Component:
    components_dir = Path(importlib.resources.path("tools.semantic.static.semantic", "components"))

    def __init__(self, name: str):
        self.name = name
        self.css = (name + (".min.css" if config.minified else ".css"))
        self.script = (name + (".min.js" if config.minified else ".js"))
        self.has_script = (self.components_dir / self.script).exists()
        self.has_css = (self.components_dir / self.css).exists()

    def gather(self):
        d = []
        if self.has_script:
            d.append(create_script(url="/static/semantic/components/" + self.script))
        if self.has_css:
            d.append(create_element('link', rel="stylesheet", href="/static/semantic/components/" + self.css))
        if self.name in extra_js.keys():
            d.append(create_element("script", inner=extra_js[self.name]))
        return (
            *d,
        )


components = {}


def check_loaded(name: str):
    if name in components.keys():
        return True
    return False


def load_component_if_needed(name: str):
    if not check_loaded(name):
        components[name] = Component(name)
