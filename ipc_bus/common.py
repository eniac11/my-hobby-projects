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
from tools.ipc import common
from tools.ipc.common import IPCHandler

ipc_handler = IPCHandler()

test_macro = ipc_handler.remote_func('test_macro')
test_object = ipc_handler.remote_object("test_object")


class MessageBus:
    def __init__(self):
        self.messages = ipc_handler.remote_object("messages")
        self.post = ipc_handler.remote_func("post")
        self.get_message = ipc_handler.remote_func("get_message")


