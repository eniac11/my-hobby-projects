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
from tools import web_framework
from tools.htmls import Page, create_script, create_div, create_element, create_image, create_link, \
    create_input
from tools.semantic import Semantic
from tools.semantic.components import load_component_if_needed
from tools.semantic.html_elements import button, create_divider, icon, label, ui, dropdown, floating, menu, item, \
    content, animated, disabled, loading, segment
from tools.semantic.layout import button_group, column, stackable, grid
from tools.web_framework import application

semantic = Semantic()

load_component_if_needed("transition")

app = web_framework.application.Application(__name__, {"semantic_": semantic.static_semantic_root})


page = Page(
    head=[
        create_script(url="/static/jquery-1.11.0.min.js"),
        semantic,
        create_element("script", inner="""
        function onsads() {
        console.log($(".reference"), $('.special.popup'));
$('.reference')
  .popup({
    popup: $('.special.popup'),
    hoverable: true
  })
;
}
""")
    ],
    body=[
        stackable(grid(create_div([
            column([
                # button class="ui button">Default</button>
                #     <button class="ui primary button">Primary</button>
                #     <button class="ui secondary button">Secondary</button>
                #     <button class="ui basic button">Basic</button>
                #     <button class="ui compact button">
                #       Compact
                #     </button>

                button(inner="Default"),
                button(inner="Primary", type_="primary"),
                button(inner="Secondary", type_="secondary"),
                button(inner="Basic", type_="basic"),
                button(inner="Compact", type_="compact"),
                create_divider(),
                icon("heart", button()),
                label("Labeled", icon("heart", button())),
                create_divider(),
                # <div class="ui buttons">
                #       <button class="ui button">Combo</button>
                #       <div class="ui floating dropdown icon button">
                #         <i class="dropdown icon"></i>
                #         <div class="menu">
                #           <div class="item">Choice 1</div>
                #           <div class="item">Choice 2</div>
                #           <div class="item">Choice 3</div>
                #         </div>
                #       </div>
                #     </div>
                button_group([
                    button(inner="Combo"),
                    dropdown(floating(button(children=[menu([
                        item(["Choice 1"]),
                        item(["Choice 2"]),
                        item(["Choice 3"])
                    ])])))
                ]),
                # <div class="ui floating search dropdown button">
                #       <span class="text">Search Dropdown</span>
                #       <div class="menu">
                #         <div class="item">Arabic</div>
                #         <div class="item">Chinese</div>
                #         <div class="item">Danish</div>
                #         <div class="item">Dutch</div>
                #         <div class="item">English</div>
                #         <div class="item">French</div>
                #         <div class="item">German</div>
                #         <div class="item">Greek</div>
                #         <div class="item">Hungarian</div>
                #         <div class="item">Italian</div>
                #         <div class="item">Japanese</div>
                #         <div class="item">Korean</div>
                #         <div class="item">Lithuanian</div>
                #         <div class="item">Persian</div>
                #         <div class="item">Polish</div>
                #         <div class="item">Portuguese</div>
                #         <div class="item">Russian</div>
                #         <div class="item">Spanish</div>
                #         <div class="item">Swedish</div>
                #         <div class="item">Turkish</div>
                #         <div class="item">Vietnamese</div>
                #       </div>
                #     </div>
                dropdown(floating(ui(children=[create_element("span", class_=["text"], inner="Search Dropdown"),
                                               menu([item(["Arabic"])])], class_=["button"])), type_="search"),
                create_divider(),
                animated(button(children=[
                    content(inner="Horizontal"),
                    content(type_="hidden", inner="Hidden")
                ])),
                animated(button(children=[
                    content(inner="Vertical"),
                    content(type_="hidden", inner="Hidden")
                ]), type_="vertical"),
                animated(button(children=[
                    content(inner="Fade In"),
                    content(type_="hidden", inner="Hidden")
                ]), type_="fade"),
                create_divider(),
                disabled(button(inner="Disabled")),
                loading(button(inner="Loading")),
                create_divider(),
                button_group([
                    button(inner="1"),
                    button(inner="2"),
                    button(inner="3"),
                ]),
                button_group([
                    icon("align left", button()),
                    icon("align center", button()),
                    icon("align right", button()),
                    icon("align justify", button()),
                ]),
                button_group([
                    button(inner="1"),
                    create_div([], class_=["or"]),
                    button(inner="2")
                ]),
                button_group([
                    button(inner="One"),
                    button(inner="Two"),
                ], class_=["two", "top", "attached"]),
                segment(class_=["attached"], children=[
                    create_image(src="/static/paragraph.png", class_=["ui", "wireframe", "image"])
                ]),
                button_group([
                    button(inner="One"),
                    button(inner="Two"),
                ], class_=["two", "bottom", "attached"]),
            ]),
            column([
                button(type_="mini", inner="Mini"),
                button(type_="tiny", inner="Tiny"),
                button(type_="small", inner="Small"),
                button(type_="large", inner="Large"),
                button(type_="big", inner="Big"),
                button(type_="huge", inner="Huge"),
                button(type_="massive", inner="Massive"),
                create_divider(),
                create_div([
                    button("yellow", inner="Yellow"),
                    button("orange", inner="Orange"),
                    button("green", inner="Green"),
                ], class_=["spaced"])
            ]),
            menu([
                item(["Brand"], class_=["header"]),
                create_link("", inner="Link", class_=["item", "active"]),
                create_link("", inner="Link", class_=["item"]),
                dropdown(item(["Dropdown", menu([
                    item(["Action"]),
                    item(["Another Action"]),
                    item(["Something else here"]),
                    create_div([], class_=["divider"]),
                    item(["Separated Line"]),
                    create_div([], class_=["divider"]),
                    item(["One more separated link"])
                ])], class_=["ui"])),
                menu([
                    item([icon("search", ui(children=[
                        create_input("text", "", placeholder="Search"),
                        button(inner="Submit")
                    ], class_=["action", "left", "icon", "input"]))]
                         )
                ], class_="right")
            ], class_=["ui"]),

        ], class_=["ui"]))),
        button(inner="Text", class_=["reference"]),

        ui(children=[create_div(["Custom Header"], class_="header"), button(inner="Click Me!")],
           class_=["special", "popup"])
    ], onload="onsads()")


@app.route("/")
def main():
    return str(page)


# @route("/static/<path:path>")
# def static(path):
#     return static_file(path, Semantic.static_semantic_root)


# run(port=5000, debug=True, reloader=True)
app.host_server(debug=True)
