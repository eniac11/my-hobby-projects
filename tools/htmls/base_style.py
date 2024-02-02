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
from .styles import *

#
# style_sheet = StyleSheet(body=StyleContainer(
#     styles={
#         **add_style_def('pre', [], {
#             **add_style_def('has(>code)', [
#                 Style('background', 'gray')
#             ])
#         })
#     },
#     classes={
#         **add_style_def('internal_link', [
#             Style("color", "black")
#         ], {
#                             **add_style_def('hover', [
#                                 Style('color', 'gray')
#                             ])
#                         }),
#
#     })
# )
style_container = StyleContainer()

with style_container:
    internal_link = (
        class_('internal_link')
        .style('color', 'black')
        .pseudo('hover')
        .style('color', 'gray')
    )

    (
        style('pre')
        .pseudo('has')
        .child('code')
        .style('background', 'gray')
    )

style_sheet = StyleSheet(style_container)
