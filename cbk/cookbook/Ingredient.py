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
from typing import Optional

from . import Stores
from .Stores import StoredItem, Store


class Ingredient:

    def __init__(self, single: str, plural: Optional[str] = None):
        self.single = single
        self.plural = plural

    def __str__(self):
        return self.single


class IngredientStore(Stores.Store[Ingredient]):

    def get(self, *args, id_: str = None, name: str = None, **kwargs) -> StoredItem[Ingredient]:
        if name is not None:
            for key, value in self.values.items():
                if value.single == name or (value.plural is not None and value.plural == name):
                    return StoredItem(self, key)
        if id_ in self.values.keys():
            return StoredItem(self, id_)

