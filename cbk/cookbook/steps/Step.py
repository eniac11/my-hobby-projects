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
import abc
from typing import Iterator


class Step(abc.ABC):

    @abc.abstractmethod
    def generate_step_info(self):
        pass


class StepIterator:

    def __init__(self, steps: list[Step]):
        self.steps = steps
        self.current_step = 0

    def next_step(self):
        self.current_step += 1

    def get_step(self):
        return self.steps[self.current_step]

    def __iter__(self) -> Iterator[Step]:
        yield from self.steps
