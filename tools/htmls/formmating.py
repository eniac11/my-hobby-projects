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

from typing import Optional

from tools.htmls.utils import Transform


class Slot(Transform):

    def __init__(self, name: Optional[str] = None):
        super().__init__()
        self.name = name
        self.filled = False

    def replace(self, elem):
        # print(elem)
        self.elem_ = elem
        self.filled = True

    def __transform__(self):
        if self.filled:
            return self.elem_
        return ""

    # def __getattr__(self, item):
    #     if self.slot.filled:
    #         return getattr(self.slot.elem_, item)
    #     return DelayedValue(self, item)

    def get_attr(self, item):
        if self.filled:
            return getattr(self.elem_, item)
        return DelayedValue(self, item)


    def __call__(self):
        return SlotValue(self)


class SlotValue:
    def __init__(self, slot: Slot):
        self.slot: Slot = slot

    def get_attr(self, item):
        if self.slot.filled:
            return getattr(self.slot.elem_, item)
        return DelayedValue(self, item)


class DelayedValue:

    def __init__(self, value: Slot, attr: str, delayed_slot_value=None):
        self.slot: Slot = value
        self.attr = attr
        self.args = None
        self.kwargs = None
        self.delayed_slot_value = delayed_slot_value
        self.func = False

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.func = True

        return self

    def get_attr(self, item):
        if self.slot.filled:
            return getattr(self.slot, item)
        return DelayedValue(self.slot, item, self)

    def get(self):
        if self.func:
            return getattr(self.slot, self.attr)(*self.args, **self.kwargs)
        return getattr(self.slot, self.attr)


def slot(name: Optional[str] = None):
    return Slot(name)


def has_slot(element):
    slots = element.internal_get_representation_blocks(Slot)
    if len(slots) > 0:
        return True
    return False


def set_slot(slotted_element, replace_elem, name: Optional[str] = None):
    slots = slotted_element.internal_get_representation_blocks(Slot)
    # print(slots)
    if len(slots) == 1:
        slots[0].replace(replace_elem)
        return
    for slot_ in slots:
        slot_: Slot
        if name is not None and slot_.name == name:
            slot_.replace(replace_elem)
