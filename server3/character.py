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
from __future__ import annotations
import uuid
from typing import Optional

from tools import semantic
from tools.htmls import *
from tools.htmls.html import ElementTransform


class LoreItem(ElementTransform):
    lore_items: dict[str, list[LoreItem]] = {}

    def __init__(self, type_: str, name: str, description: list[Element] | str, *, short_name: Optional[str] = None):
        self.id = uuid.uuid4()

        name = transform_block_to_text_block(name)
        description: list[TextBlock] | TextBlock = transform_block_to_text_block(description)
        if short_name is not None:
            short_name = transform_block_to_text_block(short_name)
        super().__init__(underline(
            create_link(f'items?category={type_}#{self.id}', data=self.id, styles=[Style('cursor', 'pointer')],
                        inner=name, class_="reference")))

        self.name = name
        self.short_name = short_name
        self.description = description
        self.type = type_

        self.__known_as = []
        # self._magic: list[LoreItem] = []
        lore_items = LoreItem.lore_items.get(type_, [])
        lore_items.append(self)
        LoreItem.lore_items[type_] = lore_items

    def documentation_text(self):
        type_ = transform_block_to_text_block(self.type)

        def header():
            if self.short_name is not None:
                return ["(", transform_text(self.short_name, str.title), ") ", transform_text(self.name, str.title)]
            return [transform_text(self.name, str.title)]

        return create_div([
            create_div([
                create_header("", children=header(), class_=["ui", "sub", "huge", "header"]),
                create_element("span", inner=transform_text(type_, str.title))
            ], class_=["header"]),
            semantic.create_divider(),
            create_div([
                create_div([*(self.document_known_as() if len(self.__known_as) > 0 else [])], class_="documentation"),
                # *(self.document_magic() if len(self._magic) > 0 else []),
                # I do this as children requires a list, so I need to coerce self.description into a list.
                *([create_p(self.description)] if type(self.description) == TextBlock else self.description),
            ], class_=["content"])
        ], id_=self.id)

    def document_known_as(self):
        return [
            create_header('Other Names', level=4),
            create_element('ul', children=[
                create_element('li', children=[
                    create_element('span', inner=val.title())
                ]) for val in self.__known_as])
        ]

    # def document_magic(self):
    #     return [
    #         create_header('Magic System', level=4),
    #         create_element('ul', children=[
    #             create_element('li', children=[
    #                 create_header(val, level=3),
    #                 val.description
    #             ]) for val in self._magic])
    #     ]

    def known_as(self, value: str):
        if value.lower() not in self.__known_as:
            self.__known_as.append(value.lower())
        return value

    # def magic(self, value: LoreItem):
    #     if value not in self._magic:
    #         self._magic.append(value)
    #     return value


class Reference(ElementTransform):

    def __init__(self, lore_item: LoreItem, type_: str, text):
        super().__init__()
        text = transform_block_to_text_block(text)

        self.lore_item = lore_item
        self.type = type_
        self.text = text

    def __transform__(self):
        return underline(
            create_link(f'items?category={self.lore_item.type}#{self.lore_item.id}', data=self.lore_item.id,
                        styles=[Style('cursor', 'pointer'), Style('color', 'red')],
                        inner=self.text, class_="reference"))


class MagicSystem(LoreItem):

    def __init__(self, name, description, magic: list[LoreItem]):
        super().__init__("MagicSystem", name, description)
        self._magic = magic

    def get_magic(self, name) -> Optional[LoreItem]:
        for magic in self._magic:
            if name == magic.name:
                return magic

    def documentation_text(self):
        doc = super().documentation_text()
        documentation = doc.get_elements_by_class_name("documentation")[0]

        documentation.add_child(
            create_element('ul', children=[*[create_list_item(children=[magic]) for magic in self._magic]]))
        return doc

    # def magic(self, name, description):
    #     magic_lore = self.get_magic(name)
    #     if magic_lore is None:
    #         magic_lore = LoreItem("magic", name, description)
    #         self._magic.append(magic_lore)
    #     return Reference(magic_lore, "magic", magic_lore.name)


def create_magic(name, description):
    return LoreItem("magic", name, description)


def create_character(name: str, description: str, **kwargs):
    return LoreItem("character", name, description, **kwargs)


def create_order(name: str, description: str, **kwargs):
    return LoreItem("order", name, description, **kwargs)


def create_faction(name: str, description: str, **kwargs):
    return LoreItem("faction", name, description, **kwargs)


def create_monolith(name, description, **kwargs):
    return LoreItem('monolith', name, description, **kwargs)


# def magic(lore_item: LoreItem, name, description):
#     magic_ = LoreItem('magic', name, description)
#     lore_item.magic(magic_)
#     return Reference(lore_item, "magic", magic_)


def create_event(name, description):
    return LoreItem('event', name, description)


def create_object(name, description):
    return LoreItem('object', name, description)


def create_item(name, description):
    return LoreItem('item', name, description)
