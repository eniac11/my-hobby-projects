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
from .common import *
from tools.ipc.common import Side


@test_macro.decorate(Side.SERVER)
def _test_macro():
    print(test_object.object)


test_object.set_side(Side.SERVER)


class test(TestClass):

    def __init__(self):
        super().__init__()
        self.text = "server1"
        self.testing.decorate(Side.SERVER)(self._testing)

    def _testing(self):
        print(self.text)


rt = test()
