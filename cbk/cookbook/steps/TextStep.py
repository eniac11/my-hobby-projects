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
from cbk.cookbook.steps.Step import Step
from tools.htmls import Element, TextBlock


class TextStep(Step):

    def __init__(self, text: Element):
        self.text = text

    def generate_step_info(self):
        # print(self.text)
        text = Element.transform_func(self.text.children)
        # text_blocks = self.text.internal_get_representation_blocks(TextBlock)
        # text = ''.join(map(lambda x: x.elem_, text_blocks))
        return text
