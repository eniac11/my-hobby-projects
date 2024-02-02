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
import typing
from typing import Optional

from tools.htmls import Element, create_div, italic, create_element, title
from tools.htmls.html import ElementTransform
from tools.semantic import styles
from tools.semantic.components import check_loaded, load_component_if_needed

div = create_div


def button(type_=None, **kwargs):
    load_component_if_needed("button")
    type_ = ("" if type_ is None else type_)
    elem = Element("button", **kwargs)
    elem.classes.extend(["ui", type_, "button"])
    return elem


def icon(name: str, elem: Element):
    load_component_if_needed("icon")
    elem.children.insert(0, italic(None, class_=[name, "icon"]))
    elem.classes.append("icon")
    return elem


def label(text, elem: Element):
    elem.children.append(text)
    elem.classes.append("labeled")
    return elem


def ui(**kwargs):
    elem = create_element("div", **kwargs)
    elem.classes.insert(0, "ui")

    return elem


def create_divider():
    load_component_if_needed("divider")
    elem = ui(class_=["divider"])
    return elem


def floating(elem):
    elem.classes.append("floating")
    return elem


def dropdown(elem, type_=None):
    load_component_if_needed("dropdown")
    elem.classes.append("dropdown")
    if type_ is not None:
        elem.classes.append(type_)
    return icon("dropdown", elem)


def menu(children, **kwargs):
    load_component_if_needed("menu")
    elem = create_div(children, **kwargs)
    elem.classes.append("menu")
    return elem


def item(children, **kwargs):
    elem = create_div(children, **kwargs)
    elem.classes.append("item")
    return elem


def animated(elem, type_=None):
    elem.classes.append('animated')
    if type_ is not None:
        elem.classes.append(type_)
    return elem


def content(type_="visible", **kwargs):
    elem = create_element("div", **kwargs)
    elem.classes.append("content")
    elem.classes.append(type_)
    return elem


def disabled(elem):
    elem.classes.append("disabled")
    return elem


def loading(elem):
    elem.classes.append("loading")
    return elem


def segment(**kwargs):
    elem = ui(**kwargs)
    elem.classes.append("segment")
    return elem


def dimmer(**kwargs):
    load_component_if_needed("dimmer")
    elem = ui(**kwargs)
    elem.classes.append("dimmer")
    return elem


def progress(label_, current_value=0, total=10, **kwargs):
    elem = ui(**kwargs, data_total=total, data_value=current_value)
    elem.classes.append("progress")

    elem.children.append(div([div([], class_=["progress"])], class_=["bar"]))
    elem.children.append(create_div([label_], class_=[styles.label()]))

    return elem


def modal(*, header=None, children=None, actions: dict[str, Element | str] = None, **kwargs):
    load_component_if_needed('modal')

    elem = ui(**kwargs)
    elem.classes.append('modal')
    elem.children.insert(0, create_div([header], class_=['header']))

    if children is not None:
        elem.children.insert(1, content(children=[*children]))

    actions_elem = create_div([], class_=['actions'])
    for key, value in actions.items():
        if type(value) == str:
            actions_elem.children.append(button(inner=value, class_=['ui', key]))
        if issubclass(value.__class__, (Element, ElementTransform)):
            value.classes.append(key)
            actions_elem.children.append(value)
    elem.children.append(actions_elem)
    return elem


def list_(type_='', **kwargs):
    elem = ui(**kwargs)
    elem.classes.append(type_)
    elem.classes.append('list')
    return elem


def steps(children, vertical: bool = False, ordered=True, **kwargs):

    elem = ui(children=children, **kwargs)
    elem.classes.append("steps")
    if vertical:
        elem.classes.append("vertical")
    if ordered:
        elem.classes.append("ordered")
    return elem



def step(title_: str, description: str, completed=True, icon_=None, **kwargs):
    if icon_ is None:
        icon_ = ""
    elem = create_div(
        [
            icon_,
            create_div([
                title(create_div([title_], class_=["title"])),
                create_div([description], class_=["description"]),
            ], class_="content")],
        **kwargs)
    elem.classes.append("step")
    if completed:
        elem.classes.append("completed")
    return elem
