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
from . import html_elements
html_elements.setup()
from tools.htmls.html_elements import create_button, create_div


Element = None
pyscript: object = None
display: object = None

def post_load():


    # button = create_button('reload', id_='reload_button')

    # print(str(button))
    # display_elem.write(str(button))
    # reload_button = Element('reload_button')
    div = create_div(['hello23'])
    div.display(display)




# print(dir(window.FileSystemEntry.filesystem.root))
