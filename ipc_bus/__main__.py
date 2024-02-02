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
import time

import requests

import ipc_bus.impl_client as impl_client

import tkinter as tk

from tools.event_system.event import Timer, update_events

root = tk.Tk()

variable = tk.StringVar(root)

lbl = tk.Label(root, textvariable=variable)
lbl.pack()

impl_client.rt.post("test")


# impl_client.rt.post("test1", "test1")
# impl_client.rt.post("test2", "test2")
# delayed_resp = impl_client.rt.get_message("test")
# delayed_resp1 = impl_client.rt.get_message("test1")
# delayed_resp2 = impl_client.rt.get_message("test2")


# impl_client.test_object('obect')
# impl_client.rt.messages('obect')

# class Timer:
#     timers = []
#
#     def __init__(self, duration: int = 5, func=None):
#         self.duration = duration
#         self.func = func
#         self.start_time = 0
#         self.running = False
#         Timer.timers.append(self)
#
#     def start(self):
#         self.start_time = time.time()
#         self.running = True
#
#     def stop(self):
#         self.running = False
#
#     def update(self):
#         if self.running:
#             current_time = time.time()
#             if current_time - self.start_time > self.duration:
#                 self.stop()
#                 if self.func is not None:
#                     self.func()


def update():
    resp1 = requests.post(url="http://127.0.0.1:5000/send_ping", headers={'Content-Type': 'application/octet-stream'},
                          data=impl_client.ipc_handler.send())
    # time.sleep(1)
    # resp1 = requests.post(url="http://127.0.0.1:5000/updates")

    impl_client.ipc_handler.receive(resp1.content)
    impl_client.ipc_handler.handle()
    timer.start()


running = True


def close():
    global running
    running = False


text_edit = tk.Entry(root)
text_edit.pack()


def post_message():
    text = text_edit.get()
    impl_client.rt.post('test')


send_btn = tk.Button(root, text='Send', command=post_message)
send_btn.pack()

close_btn = tk.Button(root, text="quit", command=close)
close_btn.pack()

timer = Timer(duration=1)
timer.subscribe(update)
timer.start()
update_events()
delayed_resp3 = impl_client.rt.get_message("test")
update_events()
root.update()
root.update_idletasks()
while running:
    if not delayed_resp3.pending:
        variable.set(delayed_resp3.value)
        delayed_resp3 = impl_client.rt.get_message("test")

    root.update()
    root.update_idletasks()
    update_events()
