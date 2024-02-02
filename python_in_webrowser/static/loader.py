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
import importlib
import os
import asyncio

import pyodide.http
import zipfile
import io

from js import document


async def download():
    data = await pyodide.http.pyfetch('/source')

    zip_buffer = io.BytesIO(await data.bytes())

    zipfile.ZipFile(zip_buffer).extractall()

    # print(os.listdir())

await download()
display_elem = Element('output').element
import static.main

# print(dir(static.main))


def event_listeners():
    from js import document
    from pyodide.ffi import create_proxy
    function_proxy = create_proxy(reload_func)

    # reload_button.onclick = reload_func
    # print(repr(document.getElementById("reload_button")))
    # document.getElementById("reload-button").addEventListener("click", function_proxy)

def load_objects():
    importlib.reload(static.main)
    static.main.Element = Element
    static.main.pyscript = pyscript
    static.main.display = display_elem
    # static.main.display = display
    # print(display)
    post_load()

def post_load():
    display_elem.innerHTML = ''
    static.main.post_load()

async def reload_func():
    print('reload')
    down = asyncio.create_task(download())

    down.add_done_callback(load_objects)
    await down




# event_listeners()
load_objects()
display_elem.innerHTML = ''
static.main.post_load()



