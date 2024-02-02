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
from pathlib import Path

from .layout import *
from .styles import *
from .core import *

static = Path("static")

text = """"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et 
dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo 
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." """

test_link = Link("www.google.com", "GoTo Google", True)

internal_link = InternalLink(create_header('hello', level=1))

# elem = create_div([
# internal_link,
# create_header('hello2', level=2),
# create_element('ul', children=[
# create_element('li', "Item" + str(i)) for i in range(10)
# ]),
# create_p(children=[
# create_text(text),
# internal_link.link("hello"),
# create_text(text)
# ]),
# test_link
# ])

# print(str(elem))


# form = Form('hello', HTTPMethod.GET, children=[
# *labeled_elem('hello', createInput('text', 'test', value='')),
# create_breakline(),
# *labeled_elem('this is a checkbox', createInput('checkbox', 'ch1', value='chk1'), reverse=True),
# create_breakline(),
# *unpack(
# create_label_radio_group(
# 'fav_language',
# [
# ['HTML', 'html'],
# ['CSS', 'css']
# ],
# new_line=True
# )),
# createInput('submit', 'hello', value='hello')
# ])

# print(str(form))

# simple page
# http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm

# style_sheet = StyleSheet(classes={**add_style_def('center', [Style('margin', 'auto')])})

# image = create_image(static / "image.png", style_def=StyleDef(style_sheet).add_class('center'))


# page = Page(head=[style_sheet], body=[
# flex([
# image,
# flex_item(image, grow=1),
# image
# ]),
# hr(),
# Link("example.com", "Link Name", True),
# create_text("is a link to another nifty site"),
# create_header("This is a Header"),
# create_header("This is a Medium  Header", level=2),
# create_text("Send me mail at"), Link("mailto:support@yourcompany.com", "support@yourcompany.com"),
# create_p("This is a new paragraph!"),
# create_p(bold("This is a new paragraph!")),
# create_breakline(),
# bold(italic(create_text("This is a new sentence without a paragraph break, in bold italics"))),
# hr()
# ])

# https://flask.palletsprojects.com/en/2.2.x/extensions/

code = """from flask_foo import Foo

foo = Foo()

app = Flask(__name__)
app.config.update(
    FOO_BAR='baz',
    FOO_SPAM='eggs',
)

foo.init_app(app)
"""


def create_nav(links):
    for key, link in links.items():
        yield link.link(link.internal_elem.inner)


def create_navbar(links):
    nav = create_element('nav', styles=[Style('margin-right', '10px')])
    ul = create_element('ul')
    for key, link in links.items():
        internal_elem = link.internal_elem
        if len(internal_elem.name) == 2 and internal_elem.name[0] == "h" and internal_elem.name[1] in "123456":
            if internal_elem.name[1] == "1":
                nav.children.append(link.link(internal_elem.inner))
            else:
                ul.children.append(create_element('li', children=[link.link(internal_elem.inner)]))
    nav.children.append(ul)
    return nav


internal_links = {"exten": InternalLink(create_header("Extensions")),
                  "find": InternalLink(create_header("Finding Extensions", level=2)),
                  "use": InternalLink(create_header("Using Extensions", level=2)),
                  "build": InternalLink(create_header("Building Extensions", level=2)),
                  }

# navbar = create_element('nav', children=[
# create_element('ul', children=[create_element('li', children=[link]) for link in list(create_nav(internal_links))])
# ]
# )
navbar = create_navbar(internal_links)

# page = Page(head=[config.style_sheet], body=[
#     flex(direction="row", item=create_div(children=[
#         navbar,
#         create_element('main', children=[
#             internal_links["exten"],
#             create_p("Extensions are extra packages that add functionality to a Flask application. For example, an extension might add support for sending email or connecting to a database. Some extensions add entire new frameworks to help build certain types of applications, like a REST API."),
#             internal_links["find"],
#             create_p(children=[
#                 create_text('Flask extensions are usually named "Flask-Foo" or "Foo-Flask". You can search PyPI for packages tagged with'),
#                 Link("pypi.org/search/?c=Framework+%3A%3A+Flask", "Framework::Flask", True)
#             ]),
#             internal_links["use"],
#             create_div([
#                     create_p('Consult each extension’s documentation for installation, configuration, and usage instructions. Generally, extensions pull their own configuration from app.config and are passed an application instance during initialization. For example, an extension called "Flask-Foo" might be used like this:'),
#                     create_element('pre', children=[
#                         create_element('code', inner=code)
#                     ])
#             ]),
#             internal_links["build"],
#             create_p(children=[
#                 create_text("While"),
#                 Link("pypi.org/search/?c=Framework+%3A%3A+Flask", "PyPI", True),
#                 create_text("contains many Flask extensions, you may not find an extension that fits your need. If this is the case, you can create your own, and publish it for others to use as well. Read"), Link("flask.palletsprojects.com/en/2.2.x/extensiondev/", "Flask Extension Development", True),
#                 create_text("to develop your own Flask extension.")
#             ])
#         ])
#     ]))
# ])
