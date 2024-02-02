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
from typing import Callable

events = []


class Event:

    def __init__(self):
        self.subscribers: list[Callable] = []

    def subscribe(self, subscriber: Callable):
        self.subscribers.append(subscriber)

    def emit(self, *args, **kwargs):
        for subscriber in self.subscribers:
            subscriber(*args, **kwargs)

    def update(self):
        pass


class Timer(Event):

    def __init__(self, duration: int = 5):
        super().__init__()
        self.duration = duration
        self.start_time = 0
        self.running = False
        events.append(self)

    def start(self):
        self.start_time = time.time()
        self.running = True

    def stop(self):
        self.running = False

    def update(self):
        if self.running:
            current_time = time.time()
            if current_time - self.start_time > self.duration:
                self.stop()
                self.emit()


def update_events():
    for event in events:
        event.update()
