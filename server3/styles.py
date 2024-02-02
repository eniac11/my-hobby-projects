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
from tools import semantic
from tools.htmls import config, base_style
from tools.htmls.styles import *

body_style_container = StyleContainer()

with body_style_container:
    body = (
        style('body')
        .style('font-family', 'sans-serif')
        .style("height", "unset !important")
        .select(".toc")
        .style("position", "fixed")
        .style("width", "250px")
        .complete()
        .complete()
        .select(".article")
        .style("margin-left", "250px")
        .complete()
        .complete()
        .child(".full.height")
        .style("display", "flex")
        .style("flex-direction", "row")

    )

    status_bar = (
        id_('status_bar')
        .style('bottom', '0')
        .style('left', '0')
        .style('position', 'fixed')
        .style('width', '100%')
        .style('height', '30px')
        .style('align-items', 'center')
        .style('display', 'flex')
        .child('*')
        .style('margin-left', '5px')
        .style('margin-right', '5px')
        .style('height', '100%')
        .style('align-items', 'center')
        .style('display', 'flex')
        .style('box-sizing', 'border-box')
        .style('padding', '5px')
        .complete()
        .complete()
        .select('*')
        .style('border', 'none')
        .style('background', 'none')
        .style('color', 'white')
        .complete()
        .complete()
        .select('a')
        .style('padding', '0px')
        .style('text-decoration', 'none')
        .complete()
        .complete()
        .select('a').select('button')
        .style('height', '100%')
        .style('width', '100%')
        # .pseudo('hover')
        # .style('opacity', "60%")
        # .style('background', "black")
    )

    window = (
        id_('window')
        # Style('width', '30%'),
        # Style('height', "80%"),
        .style('top', "0")
        .style('left', "0")
        .style("position", "absolute")
        # Style("margin", "20%"),
        # Style("background", "lightgray")
        .style("align-items", "center")
        .style("justify-content", "center")
        .style('height', '100%')
        .style('width', '100%')
        .style("pointer-events", "none")

        .child('div')
        .style('height', '80%')
        .style('width', '80%')
        .style("background", "gray")
        .style("pointer-events", "auto")
    )

    # hover = (
    #     id_('hover')
    #     .style('display', 'none')
    #     .style('position', 'absolute')
    #     .style('width', '30%')
    #     .style('max-height', '20%')
    #     .style('background', 'black')
    #     .style('color', 'white')
    #     .style('padding', '10px')
    #     .style('padding-top', '0px')
    #     .style('overflow-y', 'auto')
    #     # could be converted to mixin
    #     # eg. SD(Border, Margin)
    #     # these would provide functions that would be added to
    #     # SD
    #     .styles(create_border(all=border_style('dotted')))
    #
    # )

    hover = (
        id_("hover")
        # .style("max-width", "50%")
    )

    reference = class_('reference')

    text_help = id_("text_help")
    html = (
        style("html")
        .style("scroll-behavior", "smooth !important")
        .style("height", "unset !important")
    )

    edit = class_('edit').pseudo('hover').style('filter', 'brightness(85%)')
    input_ = (
        style('input')
        .select('.edit')
        .style('display', 'inline')
        .complete().complete()
        .select('.edit')
        .pseudo('hover')
        .style('filter', 'none')
    )

    ters = id_('ters').style('margin-bottom', '60px')

    #body_style_container.add(body)
    #body_style_container.add(input_)
    ## body_style_container.add(status_bar)
    ## body_style_container.add(window)
    #body_style_container.add(hover)
    #body_style_container.add(html)
    #body_style_container.add(text_help)
    #body_style_container.add(edit)
    #body_style_container.add(ters)

    dark_scheme = MediaQuery("(prefers-color-scheme: dark)")
    dark_scheme.add(
        html.override()
        .style('padding', '0px')
        # .style('height', '100%')
        .style('margin', '0px')
    )

    dark_scheme.add(
        body.override()
        # .style('padding', '1em')
        .style('margin', '0px')
        .style('box-sizing', 'border-box')
        .style("background", '#131516 !important')
        .style('color', 'white !important')
    )
    dark_scheme.add(
        style('a')
        .style('color', '#3391ff')
    )
    dark_scheme.add(text_help.override().style('padding-left', "10px"))
    dark_scheme.add(reference.override().style('color', "white"))
    # dark_scheme.add(status_bar.override().style('background', 'rgb(73, 79, 82)'))

    print_query = MediaQuery("print")

    print_query.add(
        style('nav')
        .style('display', 'none')
    )

    # print_query.add(
    #     body.override()
    #     .child('ul')
    #     .style('display', 'none')
    # )

    print_query.add(
        id_('test')
        .child('ul')
        .style('display', 'none')
    )

    print_query.add(
        reference.override()
        .style('color', 'black')
    )

    print_query.add(
        status_bar.override()
        .style('display', 'none')
    )

    #print_query.add(class_('toc').style('display', 'none'))

    base_style.internal_link = class_('internal_link')

config.style_sheet = StyleSheet(body_style_container,
                                [dark_scheme, print_query, semantic.styles.semantic_style_container])
