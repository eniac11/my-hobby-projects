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
import sys
sys.setrecursionlimit(4000)

import json
import zipfile
from pathlib import Path
from typing import Literal

from cbk.cookbook import manifest, steps
from cbk.cookbook.ConfigProvider import ConfigProvider
from cbk.cookbook.Stores import Provider, Store, StoredItem
from cbk.cookbook.units import Measure, Units, TimeUnit, Duration
from tools.htmls import Element, create_element, slot
from .Ingredient import IngredientStore, Ingredient
from .Recipe import RecipeStore, Recipe, IngredientItem
from tools.htmls.utils import ListTransform


def save_config(unit_system: Literal["imperial", "metric"]):
    config = {
        "unit_system": unit_system
    }
    return json.dumps(config)


def save_cookbook(cookbook_path: Path, providers: list[Provider]):
    zfs = zipfile.ZipFile(cookbook_path, mode='w')
    d = {}
    for provider in providers:
        d[provider.provider_name] = provider.save(zfs)
    manifest.save_impl(zfs, d)
    zfs.close()


def load_cookbook(cookbook_path: Path) -> list[Provider]:
    zfs = zipfile.ZipFile(cookbook_path, mode='r')
    fest = manifest.load_impl(zfs)
    providers = []
    if len(fest.get_elements_by_name('providers')[0].children) > 0:
        for provider in fest.get_elements_by_name('provider'):
            providers.append(Provider.load(zfs, provider))
    # ConfigProvider.load(zfs, Element)
    zfs.close()
    return providers

def join(sep, items):
    items_ = []
    length = len(items)
    if length > 1:
        for item in items[:-1]:
            items_.append(item)
            items_.append(sep)
        items_.append(items[-1])
    else:
        items_.extend(items)
    # print(items)
    return items_

def recipe_napoli_sauce(ingredient_provider):
    recipe2 = Recipe("Napolitano sauce", "An Italian tomato base pasta sauce.")
    recipe2.add_ingredient(Tomato :=
                           IngredientItem(ingredient_provider.get(name="Tomato"), Measure(2, Units.Tin),
                                          ["whole peeled"]))
    recipe2.add_ingredient(Garlic :=
                           IngredientItem(ingredient_provider.get(name="Garlic"), Measure(10, Units.None_),
                                          ["crushed"]))
    recipe2.add_ingredient(Oil := IngredientItem(ingredient_provider.get(name="Olive Oil"), Measure(115, Units.None_)))
    recipe2.add_ingredient(
        Onion := IngredientItem(ingredient_provider.get(name="Onion"), Measure(1, Units.Count), ["chopped"]))
    recipe2.add_ingredient(Pepper := IngredientItem(ingredient_provider.get(name="Pepper"), Measure(10, Units.Pinch)))
    recipe2.add_ingredient(Salt := IngredientItem(ingredient_provider.get(name="Salt"), Measure(10, Units.Pinch)))
    recipe2.add_ingredient(Ori := IngredientItem(ingredient_provider.get(name="Origanum"), Measure(10, Units.Pinch)))
    recipe2.add_ingredient(Basil := IngredientItem(ingredient_provider.get(name="Basil"), Measure(10, Units.Pinch)))
    recipe2.add_ingredient(
        Herbs := IngredientItem(ingredient_provider.get(name="Mixed Herbs"), Measure(10, Units.Pinch)))

    recipe2.add_step(steps.TextStep(create_element("root", children=[
        "Fry ", Onion, " and ", Garlic, " in ", Oil, " until golden brown in a pan."
    ])))

    recipe2.add_step((steps.TextStep(create_element("root", children=[
        "Add the 2 ", Tomato.ingredient.get().single, " tins. Add ", *join(', ', [Pepper, Salt, Ori, Basil, Herbs])
    ]))))

    recipe2.add_step(steps.DurationStep(Duration(1, TimeUnit.Hour), create_element("root", children=[
        "Cook for ", slot("duration")
    ])))

    recipe2.add_step(steps.TextStep(create_element("root", children=[
        "Finaly pore sauce into a bowl and blitz until all tomato chunks are gone."
    ])))

    return recipe2


def main():
    config_provder = ConfigProvider()
    recipe_provider: Provider[Store[Recipe]] = Provider("recipe", RecipeStore)
    ingredient_provider: Provider[Store[Ingredient]] = Provider("ingredient", IngredientStore)
    ingredient_provider.register_store(IngredientStore('other'))

    # unit = config_provder.get(name="unit_system")
    # unit.get().value = "metric"

    # cbk = Cookbook()
    # cbk.ingredients.add(Ingredient("Steak", "Steaks"))
    ingredient_provider.add(Ingredient("Leek", "Leeks"))
    ingredient_provider.add(Ingredient("Potato", "Potatoes"))
    ingredient_provider.add(Ingredient("Salt"))
    ingredient_provider.add(Ingredient("Pepper"))
    ingredient_provider.add(Ingredient("Butter"))

    ingredient_provider.add(Ingredient("Tomato", "Tomatoes"))
    ingredient_provider.add(Ingredient("Garlic"))
    ingredient_provider.add(Ingredient("Onion", "Onions"))
    ingredient_provider.add(Ingredient("Origanum"))
    ingredient_provider.add(Ingredient("Basil"))
    ingredient_provider.add(Ingredient("Mixed Herbs"))
    ingredient_provider.add(Ingredient("Olive Oil"))

    ingredient_provider.add(Ingredient("Mutagen"), store_name="other")

    recipe = Recipe("Potato and Leek Soup", 'A short description')
    recipe.add_ingredient(IngredientItem(ingredient_provider.get(name="Leek"), Measure(4, Units.Count)))
    recipe.add_ingredient(IngredientItem(ingredient_provider.get(name="Potato"), Measure(10, Units.Count)))
    recipe.add_ingredient(IngredientItem(ingredient_provider.get(name="Butter"), Measure(115, Units.Grams)))
    recipe.add_ingredient(IngredientItem(ingredient_provider.get(name="Salt"), Measure(10, Units.Pinch)))
    recipe.add_ingredient(IngredientItem(ingredient_provider.get(name="Pepper"), Measure(10, Units.Pinch)))

    # cbk.recipes.add(recipe)

    for step in recipe_napoli_sauce(ingredient_provider).iter_steps():
        print(step.generate_step_info())

    recipe_provider.add(recipe)
    recipe_provider.add(recipe_napoli_sauce(ingredient_provider))
    # recipe.print_ingredients()

    # print(recipe_provider.get(name="Soup").get())
    save_cookbook(Path('test2.zip'), [recipe_provider, ingredient_provider])


def load_test():
    providers = load_cookbook(Path('test2.zip'))
    for provider in providers:
        print(provider.provider_name.title() + 's')
        for item in provider:
            print(' -', item.get(), *(["/", item.get().plural] if isinstance(item.get(), Ingredient) else []))
            if isinstance(item.get(), Recipe):
                for step in item.get().iter_steps():
                    print("\t", step.generate_step_info())
        print()


if __name__ == '__main__':
    main()
