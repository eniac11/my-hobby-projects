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
import copy
import string
import time
import tracemalloc
from dataclasses import dataclass
from typing import Callable, Optional, Any, Type

from tqdm import tqdm

import tools
import tools.utils
from tools.htmls import slot, Slot, SlotValue

func_type = Callable[[Optional[Any]], None]


@dataclass
class Config:
    num_iters: int = 100


class Stat:

    def __init__(self, name: str, default, processors: Optional[list[Callable[[Any], Any]]] = None):
        self.name = name
        self.value = default
        self.processors = processors

    def set(self, value):
        self.value = value

    def get(self):
        return self.value

    def process(self):
        value = self.get()

        if self.processors is not None:
            for processor in self.processors:
                value = processor(value)

        return value

    def key(self):
        return "\u001b[1m" + self.name + "\u001b[0m"

    def __str__(self):

        return f"{self.key()}: {self.process()}"


class StatContainer:

    def __init__(self, stats: list[Stat]):
        self.stats = stats

    def get(self, name):
        for stat in self.stats:
            if name == stat.name:
                return stat

    def __str__(self):

        return '\n'.join(map(str, self.stats))


class TimeStat(Stat):

    def __init__(self, name: str, default=0, processors: Optional[list[Callable[[Any], Any]]] = None,
                 format: string.Template = '{mS} ms {µS} µs'):
        super().__init__(name, default, processors)
        self.format = format

    def __str__(self):
        return f"{self.key()}: {tools.utils.strfdelta(tools.utils.tmdelta(self.process()), self.format)}"


class MemStat(Stat):

    def __init__(self, name: str, default=0, processors: Optional[list[Callable[[Any], Any]]] = None, ):
        super().__init__(name, default, processors)

    def __str__(self):
        return f"{self.key()}: {tools.utils.convert_size(self.process())}"


class Profile:

    def __init__(self, func: func_type, name: str, stats: StatContainer = StatContainer([]),
                 data: Optional[Any] = None):
        self.name = name
        self.func = func
        self._config = slot()
        self.config = self._config()
        self.data = data
        self.stats = stats

    def start(self):
        return copy.deepcopy(self.data)

    def run(self):
        for i in tqdm(range(self.config.num_iters), desc=self.name, total=self.config.num_iters):
            data = self.start()
            self.func(data)
            self.end()

    def end(self):
        pass

    def set_config(self, config):
        self._config.replace(config)


def avg(config: SlotValue):
    def avg_(value):
        return value / config.num_iters

    return avg_


class TimeProfile(Profile):

    def __init__(self, func: func_type, name: str, data: Optional[Any]):
        super().__init__(func, name, data=data)
        self.stats = StatContainer([
            TimeStat("total_time"),
            TimeStat("avg_time", processors=[avg(self.config)])
        ])
        self.start_time = 0
        self.original_start_time = 0

    def start(self):
        data = super().start()
        self.start_time = time.perf_counter_ns()
        self.original_start_time = self.start_time
        return data

    def run(self):
        super().run()
        self.stats.get("avg_time").set(self.stats.get("total_time").get())
        self.stats.get("total_time").set(time.perf_counter_ns() - self.original_start_time)

    def end(self):
        end_time = time.perf_counter_ns()
        self.stats.get("total_time").set(self.stats.get("total_time").get() + end_time - self.start_time)


class MemProfile(Profile):

    def __init__(self, func: func_type, name: str, data: Optional[Any] = None):
        super().__init__(func, name, data=data)
        self.stats = StatContainer([
            MemStat("avg_mem", processors=[avg(self.config)]),
            MemStat("total_mem")

        ])

    def run(self):
        super().run()
        self.stats.get("avg_mem").set(self.stats.get("total_mem").get())

    def start(self):
        data = super().start()
        tracemalloc.start()
        return data

    def end(self):
        self.stats.get("total_mem").set(self.stats.get("total_mem").get() + tracemalloc.get_traced_memory()[0])
        tracemalloc.stop()


def results(res: dict[str, StatContainer]):
    s = ""
    for name, container in res.items():
        s += "test \u001b[4m" + name + "\u001b[0m\n"
        s += str(container) + "\n"
    return s


class Profiler:

    def __init__(self, config: Optional[Config] = None):
        self.profiles: list[Profile] = []
        self.config = config
        if config is None:
            self.config = Config()

    def register_profile(self, profile: Profile):
        profile.set_config(self.config)
        self.profiles.append(profile)

    def profile_func(self, profile_cls: Type[Profile], name, data: Optional[Any] = None) -> \
            Callable[[Callable], Profile]:
        def wrapper(func):
            self.register_profile(profile_cls(func, name, data))
            return func

        return wrapper

    def run(self, profiles: Optional[list[str]] = None):
        profiles_ = self.profiles
        if profiles is not None:
            profiles_ = [profile for profile in self.profiles if profile.name in profiles]

        for profile in profiles_:
            profile.run()
        profiles_ = {profile.name: profile.stats for profile in profiles_}
        return results(profiles_)
