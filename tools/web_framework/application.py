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
import hashlib
import time

from math import floor
from pathlib import Path
from typing import Callable

from tools.htmls import Form, HTTPMethod, Element_Constructor, Page, create_header
from tools.web_framework import bottle


class BotRequest(bottle.LocalRequest):

    @property
    def method(self) -> HTTPMethod:
        return HTTPMethod(super().method)


bottle.request = BotRequest()
from tools.web_framework.bottle import parse_date, HTTPResponse, request, Bottle, static_file
from tools.web_framework.form import parse_form


class ErrorPages:

    def __init__(self, app: Bottle):
        self.app = app

    def __setitem__(self, key: int, value: list[Element_Constructor]):
        page = Page(body=[
            create_header("Error " + str(key)),
            *value
        ])

        self.app.error(key)(lambda error:str(page))


class Application:

    def __init__(self, name, static_roots: dict[str, Path]):
        self.name = name
        self.app = Bottle()
        self.static_roots = static_roots
        self.app.route("/static/<path:path>")(self.static)
        self.route = self.app.route
        self.error_pages = ErrorPages(self.app)

    def host_server(self, host='127.0.0.1', port=5000, debug=False):
        if debug:
            self.app.run(host=host, port=port, debug=True, reloader=True)
        else:
            self.app.run(host=host, port=port)

    def form_route(self, form: Form, *args, **kwargs):
        @self.route(form.url, *args, **kwargs)
        def wrapper(*args_, **kwargs_):
            f: Form = parse_form(form, request)
            if request.method == HTTPMethod.GET:
                return f.get(form=f, *args_, **kwargs_)
            if request.method == HTTPMethod.POST:
                return f.post(form=f, *args_, **kwargs_)

        return wrapper

    def static(self, path):
        path_ = Path(path)

        if len(path_.parents) > 1:
            if path_.parents[-2].name in self.static_roots.keys():
                return static_file(path, self.static_roots[path_.parents[-2].name])
        if "default" in self.static_roots.keys():
            return static_file(path, self.static_roots["default"])
        return static_file(path, list(self.static_roots.values())[0])


last_modifiedes = {}


def static(data):
    hash = hashlib.sha256(data.encode()).hexdigest()
    if hash not in last_modifiedes.keys():
        last_modifiedes[hash] = time.time()

    t = last_modifiedes[hash]
    lm = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(t))

    headers = dict()
    ims = request.environ.get('HTTP_IF_MODIFIED_SINCE')
    headers['Last-Modified'] = lm
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
    if ims is not None and floor(ims) >= floor(t):
        return HTTPResponse(status=304, **headers)
    return HTTPResponse(str(data), **headers)
