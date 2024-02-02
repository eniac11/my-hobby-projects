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
from cbk.cookbook.steps import TextStep
from cbk.cookbook.steps.Step import Step
from cbk.cookbook.units import Duration
from tools.htmls import Element, TextBlock, set_slot
from tools.htmls.utils import transform


class DurationStep(TextStep):

    def __init__(self, duration: Duration, text: Element):
        super().__init__(text)
        self.duration: Duration = duration

    def generate_step_info(self):
        set_slot(self.text, self.duration, "duration")
        text = Element.transform_func(self.text.children)
        # super().generate_step_info()
        # print(text)
        # print(self.text)
        text_blocks = text
        # text = ''.join(map(lambda x: x.elem_, text_blocks))
        return text_blocks
