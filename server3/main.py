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
import configparser
import pickle
from pathlib import Path

from tools import semantic
from tools.htmls import *
from .StoryClassess import Chapter
# from tools.htmls.styles import create_border, border_style, StyleDef


from .character import *

from .story import story, internal_links


import server3.styles as misc

# style_sheet = StyleSheet(body=StyleContainer(styles_={
#     **add_style_def('body', [
#         Style('font-family', 'sans-serif')
#     ]),
#     **add_style_def('.status_bar > *', [
#         Style('margin-left', '5px'),
#         Style('margin-right', '5px'),
#         Style('height', '100%'),
#         # Style('background', 'darkgray'),
#         Style('align-items', 'center'),
#         Style('display', 'flex'),
#         Style('box-sizing', 'border-box'),
#         Style('padding', '5px')
#     ]),
#     **add_style_def('.status_bar *', [
#         Style('border', 'none'),
#         Style('background', 'none'),
#         Style('color', 'white'),
#     ]),
#     **add_style_def('.status_bar a', [
#         Style('padding', '0px'),
#         Style('text-decoration', 'none')
#
#     ]),
#     **add_style_def('.status_bar a button', [
#         Style('height', '100%'),
#         Style('width', '100%')
#
#     ], psuedo=add_style_def('hover', [
#         Style('opacity', "60%"),
#         Style('background', "black")
#     ])),
#     **add_style_def('#window > div', [
#         Style('height', '80%'),
#         Style('width', '80%'),
#         Style("background", "gray"),
#         Style("pointer-events", "auto")
#     ])
# },
#     ids={
#         **add_style_def('hover', [
#             Style('display', 'none'),
#             Style('position', 'absolute'),
#             Style('width', '30%'),
#             Style('max-height', '20%'),
#             Style('background', 'black'),
#             Style('color', 'white'),
#             Style('padding', '10px'),
#             Style('padding-top', '0px'),
#             Style('overflow-y', 'auto'),
#             *create_border(all=border_style('dotted'))
#         ]),
#         **add_style_def('window', [
#             # Style('width', '30%'),
#             # Style('height', "80%"),
#             Style('top', "0"),
#             Style('left', "0"),
#             Style("position", "absolute"),
#             # Style("margin", "20%"),
#             # Style("background", "lightgray")
#             Style("align-items", "center"),
#             Style("justify-content", "center"),
#             Style('height', '100%'),
#             Style('width', '100%'),
#             Style("pointer-events", "none")
#
#         ])
#     },
#     classes={
#         **add_style_def('status_bar', [
#             Style('bottom', '0'),
#             Style('left', '0'),
#             Style('position', 'fixed'),
#             Style('width', '100%'),
#             Style('height', '30px'),
#             Style('align-items', 'center'),
#             Style('display', 'flex'),
#
#             # Style('padding', '5px')
#         ])
#     }),
#     containers=[
#         MediaQuery("(prefers-color-scheme: dark)",
#                    styles_={
#                        **add_style_def('body', [
#                            Style('padding', '1em'),
#
#                            Style('margin', '0px'),
#                            Style('box-sizing', 'border-box'),
#
#                            Style("background", '#131516'),
#                            Style('color', 'white')
#                        ]),
#                        **add_style_def('html', [
#                            Style('padding', '0px'),
#                            Style('height', '100%'),
#                            Style('margin', '0px')
#                        ]),
#                        **add_style_def('a', [
#                            Style('color', '#3391ff')
#                        ]),
#                        **add_style_def(".sidepanel .closebtn", [
#                            Style("position", "absolute"),
#                            Style("top", "0"),
#                            Style("right", "25px"),
#                            Style("font-size", "36px")
#                        ])
#                    },
#                    ids={
#                        **add_style_def('text_help', [
#                            Style('padding-left', '10px')
#                        ]),
#
#                    },
#                    classes={
#                        **add_style_def('reference', [
#                            Style('color', 'white')
#                        ]),
#                        **add_style_def('status_bar', [
#                            Style('background', 'rgb(73, 79, 82)')
#                        ])
#                    }),
#         MediaQuery("(prefers-color-scheme: light)",
#                    classes={
#                        **add_style_def('reference', [
#                            Style('color', 'black')
#                        ])
#                    }),
#         MediaQuery("print",
#                    styles_={
#                        **add_style_def('nav', [
#                            Style('display', 'none')
#                        ]),
#                        **add_style_def('body > ul', [
#                            Style('display', 'none')
#                        ])
#                    },
#                    classes={
#                        **add_style_def('reference', [
#                            Style('color', 'black')
#                        ]),
#                        **add_style_def('status_bar', [
#                            Style('display', 'none')
#                        ])
#                    })
#     ])
# config.style_sheet = style_sheet

from .styles import *

# config.style_sheet = StyleSheet(body_style_container)
# config.style_sheet.containers.append(dark_scheme)

setup = """$(document)
  .ready(function() {
      // add popup to show name
      $('.ui:not(.container, .grid)').each(function() {
        $(this)
          .popup({
            on        : 'hover',
            variation : 'small inverted',
            exclusive : true,
            content   : $(this).attr('class')
          })
        ;
      });
  })
;"""

scripts = [
    create_script(url="/static/jquery-3.6.1.js"),
    create_script(url="/static/jquery.hotkeys.js"),
    create_script(url="/static/hoverintent.js"),
    create_script(url="/static/functions.js"),
    create_script(url="/static/popup.js"),
    create_script(url="/static/contextmenu.js"),
    create_script(url="/static/editor.js"),

    # create_script(url="/static/semantic/semantic.js"),
    # create_script(url="/static/semantic/components/popup.js"),
    # create_script(url="/static/semantic/semantic.css")
    # create_element("script", inner=setup)
]

html_story = flex_item(create_div(story), grow=1)


def create_help_text():
    items = []
    for category in LoreItem.lore_items.values():
        items.extend(map(lambda x: x.documentation_text(), category))
    return items


def get_word_count():
    text_blocks = html_story.internal_get_representation_blocks(TextBlock)
    # print(text_blocks)
    count = 0
    for text_block in text_blocks:
        text = text_block.elem_
        count += len(text.split())
    return count


def count_stats():
    text_blocks = html_story.internal_get_representation_blocks(TextBlock)
    count = 0
    count_no_spaces = 0
    for text_block in text_blocks:
        text = text_block.elem_
        # print(text)
        count += len(text)
        count_no_spaces += len(text.replace(" ", ""))

    return semantic.ui(children=[
        semantic.item(["Word Count: ", get_word_count()]),
        semantic.item(["Character Count: ", count]),
        semantic.item(["Character Count (no spaces): ", count_no_spaces])
    ], class_=["list"])


stats = count_stats()


def status_bar():
    return semantic.menu([
        semantic.menu([
            semantic.item(["Word Count: " + str(get_word_count())],
                          class_=reference(), data=stats.get_id(), data_position="top center"),  # class reference
        ], class_=["right"])
    ], id_=misc.status_bar(), class_=["ui", "bottom", "fixed", "borderless"])


###with Path('story.pickle').open("rb") as f:
    ###unpickled_story: list[Chapter] = pickle.load(f, fix_imports=True)
toc = create_div([
                    semantic.ui(children=[
                        semantic.menu([
                            semantic.item([internal_link]) for internal_link in internal_links
                        ], class_=["ui", "vertical"], id_="sticky_menu")], class_=["segment", "mmenu"])
                ], class_=["toc", "left", "ui", "attached", "rail"])

page = Page(
    head=[
        config.style_sheet,

        create_element("link", rel="stylesheet", href="/static/styles.css"),
        # create_element("link", rel="stylesheet", href="/static/semantic/components/popup.css"),
        *scripts
    ],
    body=[
        semantic.ui(children=[
            create_div([
                # <div class="ui icon button" data-content="Add users to your feed">
                #   <i class="add icon"></i>
                # </div>


                create_div([
                    semantic.ui(
                        children=[
                            create_div(story)
                        ],
                        styles=[
                            Style('height', '100%')
                        ],
                        class_=["container"])
                ], id_="test")
            ], class_=["ui", "segment"], id_="ters")], class_=["text", "container"]),

        create_div(
            [*create_help_text(), stats],

            styles=[
                Style('display', 'none')
            ]
        ),
        semantic.ui(id_=hover(), class_=["popup", "flowing"]),
        # semantic.modal(
        #     header='Profile Picture',
        #     children=[
        #         create_div([], class_=['description'])
        #     ],
        #     actions={'deny': 'Nope', 'positive': 'Yep that\'s Me'}, id='history-modal')
    ],
    onload="setupPopupCallbacks()"

)


# page.body.classes.append("pushable")


def display_lore():
    div = create_div([])
    for category in LoreItem.lore_items.keys():
        div.add_child(create_header(category.title()))
        for item in LoreItem.lore_items[category]:
            div.add_child(item.documentation_text())
    return div


def display_category(category):
    return Page(head=[
        config.style_sheet,
        *scripts
    ],
        body=[
            create_header(category.title()),
            *[
                create_div([
                    semantic.create_divider(),
                    item.documentation_text()
                ])
                for item in LoreItem.lore_items[category]
            ],
            semantic.create_divider(),
        ], onload="setupPopupCallbacks()")


def display_categories():
    return Page(head=[
        config.style_sheet,
        *scripts
    ],
        body=[
            create_element("ul", children=[
                *[
                    create_element('li', create_link("?category=" + item, item.title()))
                    for item in LoreItem.lore_items.keys()
                ]
            ])
        ], onload="setupPopupCallbacks()")


objects = Page(body=[
    display_lore()
])
