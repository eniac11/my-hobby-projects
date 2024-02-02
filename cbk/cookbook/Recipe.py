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
import typing
from dataclasses import dataclass, field

from tools.htmls import Transform, TextBlock
from .Ingredient import Ingredient
from .Stores import StoredItem, Store, T
from .steps.Step import Step, StepIterator
from .units import Measure


@dataclass
class IngredientItem(Transform):
    ingredient: StoredItem[Ingredient]
    measure: Measure
    qualifiers: list[str] = field(default_factory=list)

    def __transform__(self):
        ingredient = self.ingredient.get()
        name = ingredient.single
        if self.measure.value > 1 and ingredient.plural is not None:
            name = ingredient.plural

        measure = self.measure.localise(self.ingredient.get())

        return TextBlock(name + (', ' + measure if measure is not None else ''))

    def __str__(self):
        return self.__transform__().elem_

    def fullname(self):
        ingredient = self.ingredient.get()
        name = ingredient.single
        if self.measure.value > 1 and ingredient.plural is not None:
            name = ingredient.plural

        return name + ', '.join(self.qualifiers) + ', ' + str(self.measure.value) + self.measure.unit.value


class Recipe:

    def __init__(self, name: str, description: str):
        self.name = name
        self.ingredients: list[IngredientItem] = []
        self.description = description

        self.steps: list[Step] = []

    def add_ingredient(self, ingredient: IngredientItem):
        self.ingredients.append(ingredient)
        return ingredient

    def add_step(self, step):
        self.steps.append(step)

    def iter_steps(self) -> StepIterator:
        return StepIterator(self.steps)

    def print_ingredients(self):
        for ingredient_item in self.ingredients:
            print(ingredient_item)

    def __str__(self):
        return self.name


class RecipeStore(Store[Recipe]):

    def get(self, *args, id_: str = None, name: str = None, **kwargs) -> StoredItem[Recipe]:
        if name is not None:
            for key, value in self.values.items():
                if value.name == name:
                    return StoredItem(self, key)
        if id_ in self.values.keys():
            return StoredItem(self, id_)
