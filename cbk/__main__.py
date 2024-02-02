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

from cbk import pages

from cbk.cookbook.Cookbook import load_cookbook
from cbk.cookbook.steps.TextStep import TextStep
from tools.web_framework.application import Application

from cbk import styles as my_styles
from tools.semantic.styles import semantic_style_container
from tools.htmls import config

config.style_sheet.containers.append(my_styles.my_container)
config.style_sheet.containers.append(semantic_style_container)

from tools.htmls import *

from cbk.cookbook.Stores import Provider, Store, StoredItem
from cbk.cookbook.units import Measure, Units
from cbk.cookbook.Ingredient import IngredientStore, Ingredient
from cbk.cookbook.Recipe import RecipeStore, Recipe, IngredientItem
from tools.semantic import Semantic

semantic = Semantic()


app = Application("cookbook", {"semantic_": semantic.static_semantic_root})

# recipe_provider: Provider[Store[Recipe]] = Provider(RecipeStore)
# ingredient_provider: Provider[Store[Ingredient]] = Provider(IngredientStore)
# # cbk = Cookbook()
# # cbk.ingredients.add(Ingredient("Steak", "Steaks"))
# ingredient_provider.add(Ingredient("Steak", "Steaks"))
# recipe_ = Recipe("Soup")
# recipe_.add_ingredient(IngredientItem(ingredient_provider.get(name="Steak"), Measure(10, Units.MiliGrams)))
# recipe_.add_step(TextStep("This is a step"))
# # cbk.recipes.add(recipe)
# recipe_provider.add(recipe_)
# recipe_.print_ingredients()
# print(recipe_provider.get(name="Soup").get())

providers = load_cookbook(Path("test2.zip"))

recipe_provider = providers[0]
ingredient_proiver = providers[1]


@app.route('/recipes')
@app.route('/recipe/<recipe_id>')
def recipes(recipe_id=None):
    recipe: StoredItem[Recipe]
    if recipe_id is None:
        page = Page(head=[config.style_sheet, create_script(url="/static/jquery-1.11.0.min.js"), semantic], body=[
            Link("/recipe/" + recipe.id, recipe.get().name) for recipe in recipe_provider
        ])

        return str(page)

    recipe: Recipe = recipe_provider.get(id_=recipe_id).get()

    page = pages.Recipe.display(recipe)
    page.head.add_child(create_script(url="/static/jquery-1.11.0.min.js"))
    page.head.add_child(semantic)
    page.head.add_child(config.style_sheet)


    return str(page)


app.host_server(debug=True)
