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
import flask
from flask import request, jsonify

from tools.htmls import *
import controlling.main as main

app = flask.Flask(__name__)


@app.route("/", methods=["POST"])
def test():
    if request.method == "POST":
        control_data = main.ControlData.deserialize(request.json)
        main.macro_group.handle(control_data)
    return ""


@app.route("/updates", methods=["POST"])
def updates():
    if request.method == "POST":
        control_data = main.ControlData.deserialize(request.json)
        return jsonify(list(map(lambda x: x.serialize(), main.macro_group.process_updates(control_data))))
    return ""


page = Page(head=[
    main.script_element
], body=main.macro_group.macros
)


@app.route("/macros")
def macros():
    return str(page)
