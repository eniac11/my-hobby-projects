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
from tools.ipc.common import Side, IPCMessage, IPCType

ipc_handler.set_side(Side.CLIENT)

@test_macro.decorate()
def _test_macro():
    print("client")


class test(MessageBus):

    def __init__(self):
        super().__init__()
        self.text = "client"
        # self.messages.set_side(Side.CLIENT)
        self.post.decorate()(self._post)
        self.get_message.decorate()(self._get_message)

    def _post(self, id_, data):
        # self.message(message)
        pass

    def _get_message(self, id_):
        print(id_)


rt = test()


# test_object.set_side(Side.CLIENT)
