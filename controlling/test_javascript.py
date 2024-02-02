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
from typing import Callable

from tools.htmls import Transform
from tools.htmls.javascript import *
from tools.htmls.javascript.api import *


updates = Variable("updates", 10)


func = Function('func', ['test'], [
    CodeBlock([
        updates.create()
    ]),
    CodeBlock([
        console.log([updates.get()], True).call()
    ])
])

script = Script([
    func
])

print(script)
