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

from tools.web_framework.application import Application
from tools.web_framework.bottle import request

from tools.htmls import *
import controlling.main as main

# Polling html js
# https://www.freecodecamp.org/news/5-ways-to-build-real-time-apps-with-javascript-5f4d8fe259f7/
app = Application('controlling', static_roots={"default": importlib.resources.path("controlling", "static")})


@app.route("/", methods=["POST"])
def test():
    if request.method == "POST":
        control_data = main.ControlData.deserialize(request.json)
        main.macro_group.handle(control_data)
    return ""


@app.route("/updates", methods=["POST"])
def updates():
    if request.method == "POST":
        # control_data = main.ControlData.deserialize(request.json)
        updates2 = main.macro_group.process_updates()
        print(updates2)
        update = []
        for macro_update in updates2:
            for control in macro_update:
                update.append(control.serialize())

        return update
    return ""


script = create_script(url="/static/test.js")

page = Page(head=[
    main.script_element,
    script
], body=[create_button('update', onclick="updates()"), *main.macro_group.macros]
)


@app.route("/macros")
def macros():
    return str(page)

app.host_server(debug=True)