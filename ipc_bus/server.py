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
from flask import Flask, request

import ipc_bus.impl_server as impl_server
from tools.ipc.common import IPCMessage

app = Flask(__name__)


# impl_server.test_object('obect')

@app.route("/post", methods=["POST"])
def post_message():
    if request.method == "POST":
        impl_server.ipc_handler.receive(request.data)
        impl_server.ipc_handler.handle()
    return ""


@app.route("/updates", methods=["POST"])
def get_updates():
    if request.method == "POST":
        return impl_server.ipc_handler.send()


@app.route("/send_ping", methods=["POST"])
def send_ping():
    if request.method == "POST":
        impl_server.ipc_handler.receive(request.data)
        impl_server.ipc_handler.handle()
        return impl_server.ipc_handler.send()
