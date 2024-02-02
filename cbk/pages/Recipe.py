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
from cbk.cookbook.Recipe import Recipe
from cbk.cookbook.steps.Step import StepIterator
from cbk import styles as my_styles

from tools.semantic.layout import button_group, column, stackable, grid
from tools.semantic import html_elements as semantic_elements

from tools.htmls import *


def method(step_iterator: StepIterator):
    return create_div([
        semantic_elements.steps([
            semantic_elements.step(
                "", "",
                completed=(True if i < step_iterator.current_step else False),
                class_=("active" if i == step_iterator.current_step else "")
            ) for i, step in enumerate(step_iterator)], vertical=True, ordered=True),
        create_element("ol", children=[
            create_list_item(inner=step.generate_step_info()) for step in step_iterator

        ])
    ], id_=my_styles.content())


def sidebar(recipe: Recipe):
    return create_div([
        create_header(recipe.name),
        create_element("ul", children=[
            create_list_item(inner=ingredient) for ingredient in recipe.ingredients
        ])
    ], id_=my_styles.sidebar())


def display(recipe: Recipe):
    return Page(body=[
        grid(semantic_elements.ui(children=[
            column(create_div([sidebar(recipe)], class_=['four', 'wide'])),
            column(create_div([method(recipe.iter_steps())]))
        ], class_=["equal", "width", "horizontally", "divided"]))
    ])
