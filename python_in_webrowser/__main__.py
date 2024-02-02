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
import importlib.resources
import json
import os
from pathlib import Path

from tools import htmls
from tools.web_framework import bottle
from tools.web_framework.application import Application

os.environ['NO_PROXY'] = '127.0.0.1'

app = Application('python_in_webrowser', {"default": importlib.resources.path("python_in_webrowser", "static")})

# <!DOCTYPE html>
# <html lang="en">
#   <head>
#     <meta charset="utf-8" />
#     <meta name="viewport" content="width=device-width,initial-scale=1" />
#
#     <title>PyScript Hello World</title>
#
#     <link rel="icon" type="image/png" href="favicon.png" />
#     <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
#
#     <script defer src="https://pyscript.net/latest/pyscript.js"></script>
#   </head>
#
#   <body>
#     Hello world! <br>
#     This is the current date and time, as computed by Python:
#     <py-script>
# from datetime import datetime
# now = datetime.now()
# now.strftime("%m/%d/%Y, %H:%M:%S")
#     </py-script>
#   </body>
# </html>

import io
import zipfile


def collect_source(sources_paths) -> list[tuple[Path, Path]]:
    source = []

    for sources_path in sources_paths:
        prune_name = Path(sources_path)
        for act_path, dirnames, filenames in os.walk(prune_name):
            act_path = Path(act_path)

            filenames.sort()
            for filename in filenames:
                if filename == "loader.py":
                    continue
                local_path = act_path.relative_to(prune_name.parents[0]) / filename
                source.append((act_path / filename, local_path))
                # print((path / filename).as_posix())
    return source





@app.route('/')
def root():
    return str(htmls.Page(
        head=[
            htmls.create_element("link", rel="stylesheet", href="https://pyscript.net/latest/pyscript.css"),
            htmls.create_script(url="https://pyscript.net/latest/pyscript.js", defer=True)
        ],
        body=[
            # htmls.create_element('py-config', type_="json", inner=collect_source()),

            # htmls.create_element("py-script", src="static/main.py"),
            htmls.create_button('reload_button',id_='reload-button', py_onClick='reload_func()'),
            htmls.create_div([], id_='output'),
            htmls.create_element("py-script", src="static/loader.py"),
        ]
    ))


@app.route('/source')
def source():
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'x', zipfile.ZIP_DEFLATED, False) as zip_file:
        for act_path, local_path in collect_source([
                Path('tools').absolute(), Path('python_in_webrowser/static').absolute()]):
            with act_path.open('rb') as f:
                zip_file.writestr(local_path.as_posix(), f.read())
    bottle.response.content_type = "application/x-zip-compressed"
    return zip_buffer.getvalue()


# print(root())

app.host_server(debug=True)
