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

import abc
import uuid
from enum import Flag
from typing import Callable, Optional, TypeVar, Iterable

from .formmating import DelayedValue
from .utils import *

__all__ = ['HTTPMethod', 'Element', 'ElementTransform', 'DelayedElementTransform', 'Element_Constructor']

from .utils import ListTransform, DelayedTransform
from .. import pyjack


class HTTPMethod(Flag):
    GET = 'GET'
    POST = 'POST'

    @classmethod
    def get_method(cls, method: HTTPMethod):
        return method.name

    def __str__(self):
        return self.name

class BaseElement(abc.ABC):

    @abc.abstractmethod
    def add_child(self, child: BaseElement):
        pass

    @abc.abstractmethod
    def add_children(self, children: list[Element]):
        pass

    @abc.abstractmethod
    def get_id(self) -> str:
        pass

    @abc.abstractmethod
    def get_element_by_id(self, id_: str) -> Element:
        pass

    @abc.abstractmethod
    def get_elements_by_class_name(self, class_name: str) -> list[Element]:
        pass

T = TypeVar("T")


class Element(BaseElement):
    def __init__(self, name, *, styles: list["Style"] = None, inner: Element | str = None,
                 children: Optional[list[Element | str]] = None,
                 single=False, class_=None, **kwargs):
        if children is not None:
            children = transform_block_to_text_block(children)
        if inner is not None:
            inner = transform_block_to_text_block(inner)
            # print(inner)

        self.name = name
        self.kwargs = kwargs
        self.kwargs = {process_variable_underscore(key): val for key, val in self.kwargs.items()}
        self.inner = inner
        self.children: list[Element | str] = children
        if children is None:
            self.children: list[Element | str] = []
        self.classes = class_

        if type(class_) not in [list, tuple]:
            self.classes = [class_]
        if class_ is None:
            self.classes = []

        self.single = single


        self.styles = styles
        if styles is None:
            self.styles = []

    def add_child(self, child: Element):
        self.children.append(child)

    def add_children(self, children: list[Element]):
        self.children.extend(children)

    def get_id(self):
        id_ = self.kwargs.get('id', None)
        if id_ is None:
            id_ = str(uuid.uuid4())
            self.kwargs['id'] = id_
        return id_

    def __transform__(self):
        self.children = self.transform_func(self.children)
        self.inner = transform(self.inner)
        return self

    @staticmethod
    def _process_kwargs(kwargs):
        for key, val in kwargs.items():

            if type(val) == DelayedValue:
                kwargs[key] = val.__get__()
        return kwargs

    @staticmethod
    def transform_func(list_: list):
        items: list[Element_Constructor] = []
        for item in list_:
            if issubclass(item.__class__, ListTransform):
                items.extend(transform(item))
            else:

                items.append(transform(item))
            # print(item)
        return ''.join(map(str, items))

    def __str__(self):
        inner = ""
        styles = ""
        classes = equatify({'class': ' '.join(self.classes)})

        if len(self.children) > 0:
            # inner += ''.join(map(str, map(transform, self.children)))
            inner += self.transform_func(self.children)
        else:
            if self.inner is not None:
                inner = transform(self.inner)

        if len(self.styles) > 0:
            styles = equatify({"style": ''.join(map(str, self.styles))})

        kwargs = equatify(self._process_kwargs(self.kwargs))
        if self.single:
            return f"<{self.name} {classes}{styles}{kwargs}/>"

        return f"<{self.name} {classes}{styles}{kwargs}>{inner}</{self.name}>"

    def get_element_by_id(self, id_: str) -> Element:
        for element in self.children:
            if issubclass(element.__class__, Element):
                if (elem := element.get_element_by_id(id_)) is not None:
                    return elem

        if id_ == self.kwargs.get("id", ""):
            return self

    def get_elements_by_class_name(self, class_name: str) -> list[Element]:
        elems = []

        if class_name in self.classes:
            elems.append(self)

        for elem in self.children:
            if issubclass(elem.__class__, Element):
                elems.extend(elem.get_elements_by_class_name(class_name))
        return elems

    def get_elements_by_name(self, elem_name: str) -> list[Element]:
        elems = []
        if elem_name == self.name:
            elems.append(self)
        for elem in self.children:
            if issubclass(elem.__class__, Element):
                elems.extend(elem.get_elements_by_name(elem_name))
            if issubclass(elem.__class__, ElementTransform):
                elem: ElementTransform
                elems.extend(elem.elem.get_elements_by_name(elem_name))
        return elems

    def internal_get_representation_blocks(self, cls: type[T]) -> Iterable[T]:
        elems = []
        if self.inner is not None:
            if type(self.inner) == cls:
                elems.append(self.inner)
            elif issubclass(self.inner.__class__, Element):
                elems.extend(self.inner.internal_get_representation_blocks(cls))
            elif issubclass(self.inner.__class__, ElementTransform):
                elems.extend(self.inner.internal_get_representation_blocks(cls))

        for child in self.children:
            if type(child) == cls:
                elems.append(child)
            elif issubclass(child.__class__, Element):
                elems.extend(child.internal_get_representation_blocks(cls))
            elif issubclass(child.__class__, ElementTransform):
                elems.extend(child.internal_get_representation_blocks(cls))

        return elems

    def internal_replace_representation_block_with_id(self, cls, id_, replacement):
        blocks = self.internal_get_representation_blocks(cls)
        for i, block in enumerate(blocks):
            if block.id == id_:
                replacement.id = id_
                pyjack.replace_all_refs(block, replacement)
                break


class ElementTransform(Transform):

    def __init__(self, elem=None):
        super().__init__(elem)

    @property
    def elem(self) -> Element:
        return transform(self)

    def internal_get_representation_blocks(self, cls):
        elems = []
        inner = self.elem.inner
        if inner is not None:
            if type(inner) == cls:
                elems.append(inner)
            elif issubclass(inner.__class__, Element):
                elems.extend(inner.internal_get_representation_blocks(cls))
            elif issubclass(inner.__class__, ElementTransform):
                elems.extend(inner.internal_get_representation_blocks(cls))

        for child in self.elem.children:
            if type(child) == cls:
                elems.append(child)
            elif issubclass(child.__class__, Element):
                elems.extend(child.internal_get_representation_blocks(cls))
            elif issubclass(child.__class__, ElementTransform):
                elems.extend(child.internal_get_representation_blocks(cls))

        return elems

    def internal_replace_representation_block_with_id(self, cls, id_, replacement):
        blocks = self.internal_get_representation_blocks(cls)
        for i, block in enumerate(blocks):
            if block.id == id_:
                replacement.id = id_
                pyjack.replace_all_refs(block, replacement)

                break

    def get_element_by_id(self, id_: str) -> Element:
        for element in self.elem.children:
            if issubclass(element.__class__, Element):
                if (elem := element.get_element_by_id(id_)) is not None:
                    return elem

        if id_ == self.elem.kwargs.get("id", ""):
            return self.elem

    def get_elements_by_class_name(self, class_name: str) -> list[Element]:
        elems: list[Element | ElementTransform] = []

        if class_name in self.elem.classes:
            elems.append(self)

        for elem in self.elem.children:
            if issubclass(elem.__class__, Element):
                elems.extend(elem.get_elements_by_class_name(class_name))
        return elems

    def get_elements_by_name(self, elem_name: str) -> list[Element]:
        elems: list[Element | ElementTransform] = []
        if elem_name == self.elem.name:
            elems.append(self)
        for elem in self.elem.children:
            if issubclass(elem.__class__, Element):
                elems.extend(elem.get_elements_by_name(elem_name))
        return elems


class DelayedElementTransform(DelayedTransform, ElementTransform):
    pass
Element_Constructor = Element