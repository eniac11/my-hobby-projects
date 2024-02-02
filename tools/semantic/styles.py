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
# from server3.misc import StyleContainer
# from tools.htmls import class_, StyleContainer
from tools.htmls.styles import class_, StyleContainer

semantic_style_container = StyleContainer()
with semantic_style_container:

    error = class_("error").style("cursor", "pointer")
    green = class_("green").style("color", "#16ab39")
    red = class_("red").style("color", "#db2828")
    blue = class_("blue").style("color", "#db2828")
    yellow = class_("yellow").style("color", "#FBBD08;")
    orange = class_("orange").style("color", "#F2711C;")

    spaced = class_("spaced").child(".button").style("margin-bottom", "1em")

    label = class_("label")

# semantic_style_container.add(green)
# semantic_style_container.add(error)
# semantic_style_container.add(red)
# semantic_style_container.add(yellow)
# semantic_style_container.add(orange)
# semantic_style_container.add(spaced)

