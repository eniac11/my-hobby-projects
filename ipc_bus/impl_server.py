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
from tools.ipc.common import Side, IPCMessage

ipc_handler.set_side(Side.SERVER)


@test_macro.decorate()
def _test_macro():
    print(test_object.object)


# test_object.set_side(Side.SERVER)


class test(MessageBus):

    def __init__(self):
        super().__init__()
        self._messages = {}
        # self.messages.set_side(Side.SERVER)
        self.post.decorate()(self._post)
        self.get_message.decorate()(self._get_message)

    def _post(self, id_, data):
        print(id_)
        self._messages[id_] = data

    def _get_message(self, id_):
        self.messages(self._messages[id_])

        return self._messages[id_]


rt = test()
# print(rt.messages.side)
