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
from tools.htmls.styles import *

body = (
    style('body')
    .style('font-family', 'sans-serif')
    .style("height", "unset !important")
    .select(".toc")
    .style("position", "fixed")
    .style("width", "250px")
    .complete()
    .select(".article")
    .style("margin-left", "250px")
    .complete()
    .child(".full.height")
    .style("display", "flex")
    .style("flex-direction", "row")

)

print(body)
