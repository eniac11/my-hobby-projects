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
from __future__ import annotations

import functools
import pickle
import time
import uuid
from enum import Enum, auto
from queue import Queue
from typing import Callable


class IPCType(Enum):
    FUNCTION = auto()
    FUNCTION_RETURN = auto()
    STRING = auto()
    OBJECT = auto()


class Side(Enum):
    SERVER = auto()
    CLIENT = auto()


class IPCMessage:
    def __init__(self, type_: IPCType, data):
        self.type = type_
        self.data = data
        self.timestamp = time.time()

    def pickle(self) -> bytes:
        return pickle.dumps(self)

    @staticmethod
    def unpickle(message: bytes) -> IPCMessage:
        return pickle.loads(message)


class IPCHandle:

    def __init__(self, ipc_handler: IPCHandler):
        self.ipc_handler = ipc_handler

    @property
    def side(self):
        return self.ipc_handler.side

    def handle(self, message):
        return False


class IPCHandler:
    def __init__(self):
        self.ipc_handles: list[IPCHandle] = []
        self.side = None
        self.in_queue = Queue()
        self.out_queue = Queue()

    def set_side(self, side: Side):
        self.side = side

    def add_handle(self, handle: IPCHandle):
        self.ipc_handles.append(handle)

    def remote_func(self, name) -> RemoteFunction:

        handle = RemoteFunction(name, self)
        self.ipc_handles.append(handle)
        return handle

    def remote_object(self, name):
        handle = RemoteObject(name, self)
        self.ipc_handles.append(handle)
        return handle

    def send(self):
        items = []
        while not self.out_queue.empty():
            item: IPCMessage = self.out_queue.get()
            items.append(item)
        return pickle.dumps(items)

    def receive(self, data: bytes):
        messages = pickle.loads(data)

        for message in messages:
            self.in_queue.put(message)

    def handle(self):
        while not self.in_queue.empty():
            message: IPCMessage = self.in_queue.get()
            for ipc_handle in self.ipc_handles:
                if ipc_handle.handle(message):
                    break
        self.clean_up_function_responses()

    def clean_up_function_responses(self):
        function_response_pos_ids = []
        for i, ipc_handle in enumerate(self.ipc_handles):
            if type(ipc_handle) == FunctionResponse:
                ipc_handle: FunctionResponse
                if not ipc_handle.pending:
                    function_response_pos_ids.append(i)
        for i in function_response_pos_ids:
            self.ipc_handles.pop(i)


class FunctionResponse(IPCHandle):

    def __init__(self, response_id, ipc_handler: IPCHandler):
        super().__init__(ipc_handler)

        self.response_id = response_id
        self.pending = True
        self.value = None
        self.ipc_handler.add_handle(self)

    def handle(self, message: IPCMessage):
        if message.type == IPCType.FUNCTION_RETURN and message.data['resp_id'] == self.response_id:
            self.pending = False
            self.value = message.data['data']
            return True
        return False


class RemoteFunction(IPCHandle):

    def __init__(self, name: str, ipc_handler: IPCHandler):
        super().__init__(ipc_handler)
        self.name = name
        self.server_func = None
        self.client_func = None
        # self.func = func
        # self.func_name = func.__name__
        # self.ipc_handler = ipc_handler

    def decorate(self):
        # self.side = side

        def wrapper(func):
            if self.side == Side.CLIENT:
                self.client_func = func
            elif self.side == Side.SERVER:
                self.server_func = func
            return self

        return wrapper

    def __call__(self, *args, **kwargs):

        if self.side == Side.CLIENT:
            self.resp_id = uuid.uuid4()
            self.ipc_handler.out_queue.put(
                IPCMessage(IPCType.FUNCTION,
                           {'name': self.name, 'resp_id': self.resp_id, 'args': args, 'kwargs': kwargs}))
            if (test := self.client_func(*args, **kwargs)) is not None:
                self.ipc_handler.out_queue.put(test)
            return FunctionResponse(self.resp_id, self.ipc_handler)
        elif self.side == Side.SERVER:
            if (test := self.server_func(*args, **kwargs)) is not None:
                self.ipc_handler.out_queue.put(test)

    def handle(self, message):
        if message.type == IPCType.FUNCTION and message.data['name'] == self.name:
            if (test := self.server_func(*message.data['args'], **message.data['kwargs'])) is not None:
                self.ipc_handler.out_queue.put(
                    IPCMessage(IPCType.FUNCTION_RETURN, {'resp_id': message.data['resp_id'], 'data': test}))
            return True
        return False


class RemoteObject(IPCHandle):

    def __init__(self, name, ipc_handler: IPCHandler):
        super().__init__(ipc_handler)

        self.object = None
        self.name = name

    def __call__(self, object):
        self.ipc_handler.out_queue.put(IPCMessage(IPCType.OBJECT, {'name': self.name, 'data': object}))

    def handle(self, message: IPCMessage):
        if message.type == IPCType.OBJECT and self.name == message.data['name']:
            self.object = message.data['data']

            return True
        return False
