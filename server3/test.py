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
import datetime
import time
import tracemalloc

from math import floor
from string import Formatter
from typing import Callable, Type

from .main import *

from time import perf_counter_ns

times = []

links = [
    Link('/', "Story"),
    Link('/items', 'Story Reference'),
    Link('/chapters', 'Chapters')
]


def create_navbar():
    return create_element('nav', children=[
        create_element('span', children=[link, " | "]) for link in links
    ])


iters = 200


def test(page):
    page.body.get_element_by_id('test').children.insert(0, create_navbar())
    page.body.get_element_by_id('test').children.insert(1, create_element('ul', children=[
        create_list_item(children=[internal_link]) for internal_link in internal_links
    ]))
    page.body.children.insert(-1, status_bar())
    str(page)


def tmdelta(delta):
    return datetime.timedelta(microseconds=(delta * 1e-6))


def strfdelta(tdelta, fmt='{D:02}d {H:02}h {M:02}m {S:02.0f}s', inputtype='timedelta'):
    """Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the stftime() method does for datetime.datetime
    objects.

    The fmt argument allows custom formatting to be specified.  Fields can
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        '{D:02}d {H:02}h {M:02}m {S:02.0f}s' --> '05d 08h 04m 02s' (default)
        '{W}w {D}d {H}:{M:02}:{S:02.0f}'     --> '4w 5d 8:04:02'
        '{D:2}d {H:2}:{M:02}:{S:02.0f}'      --> ' 5d  8:04:02'
        '{H}h {S:.0f}s'                       --> '72h 800s'

    The inputtype argument allows tdelta to be a regular number instead of the
    default, which is a datetime.timedelta object.  Valid inputtype strings:
        's', 'seconds',
        'm', 'minutes',
        'h', 'hours',
        'd', 'days',
        'w', 'weeks'
    """

    # Convert tdelta to integer seconds.
    if inputtype == 'timedelta':
        remainder = tdelta.total_seconds()
    elif inputtype in ['s', 'seconds']:
        remainder = float(tdelta)
    elif inputtype in ['m', 'minutes']:
        remainder = float(tdelta) * 60
    elif inputtype in ['h', 'hours']:
        remainder = float(tdelta) * 3600
    elif inputtype in ['d', 'days']:
        remainder = float(tdelta) * 86400
    elif inputtype in ['w', 'weeks']:
        remainder = float(tdelta) * 604800

    f = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt)]
    possible_fields = ('Y', 'm', 'W', 'D', 'H', 'M', 'S', 'mS', 'µS')
    constants = {'Y': 86400 * 365.24, 'm': 86400 * 30.44, 'W': 604800, 'D': 86400, 'H': 3600, 'M': 60, 'S': 1,
                 'mS': 1 / pow(10, 3), 'µS': 1 / pow(10, 6)}
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in constants:
            Quotient, remainder = divmod(remainder, constants[field])
            values[field] = int(Quotient) if field != 'S' else Quotient + remainder
    return f.format(fmt, **values)


class Test:

    def __init__(self, iters):
        self.tests: dict[str, tuple[Callable[[], None], dict]] = {}
        self.iters = iters

    def register_test(self, name: str):
        self.tests[name] = [None, {}]

        def wrapper(func):
            def sub_wrapper():
                self.tests[name][1].update(func())

            self.tests[name][0] = sub_wrapper

            return sub_wrapper

        return wrapper

    def run(self):
        for name, test in self.tests.items():
            func = test[0]
            func()

    def __str__(self):
        s = ""
        for name, results in self.tests.items():
            s += "test \u001b[4m" + name + "\u001b[0m\n"
            for key, val in results[1].items():
                s += "\u001b[1m" + key + ":\u001b[0m " + val + "\n"
        return s


tests = Test(iters)


@tests.register_test("time_perf")
def time_perf():
    timing = 0
    complete_time_start = time.perf_counter_ns()

    for i in range(iters):
        copy_page = copy.deepcopy(page)
        start_time = time.perf_counter_ns()

        test(copy_page)

        end_time = time.perf_counter_ns()
        timing += end_time - start_time
    return {
        "avg_time": strfdelta(tmdelta(timing / iters), '{mS} ms {µS} µs'),
        "total_time": strfdelta(tmdelta((time.perf_counter_ns() - complete_time_start)), '{mS} ms {µS} µs')
    }


# print(floor((timing / iters) * 1e-6), "ms", floor((time.perf_counter_ns() - complete_time_start) * 1e-6))
# print(tmdelta(timing / iters), tmdelta((time.perf_counter_ns() - complete_time_start)))




@tests.register_test("memory")
def test_memory():
    total_memory = 0
    complete_time_start = time.perf_counter_ns()

    for i in range(iters):
        copy_page = copy.deepcopy(page)
        tracemalloc.start()

        test(copy_page)

        total_memory += tracemalloc.get_tracemalloc_memory()
        tracemalloc.stop()

    return {
        "total_mem": convert_size(total_memory), "avg_mem": convert_size(total_memory / iters),
        "total_time": strfdelta(tmdelta((time.perf_counter_ns() - complete_time_start)), '{mS} ms {µS} µs')
    }


# tests.run()
# print(tests)

from tools.profiler import *

config_ = Config()

profiler = Profiler(config_)


@profiler.profile_func(TimeProfile, "time_perf", data=page)
@profiler.profile_func(MemProfile, "memory", data=page)
def test_(data):
    data.body.get_element_by_id('test').children.insert(0, create_navbar())
    data.body.get_element_by_id('test').children.insert(1, create_element('ul', children=[
        create_list_item(children=[internal_link]) for internal_link in internal_links
    ]))
    data.body.children.insert(-1, status_bar())
    str(page)


# profiler.register_profile(test_)

print(profiler.run())

# prof = profiler.profiles[0]
# print("avg_time", strfdelta(tmdelta(prof.timing / iters), '{mS} ms {µS} µs'))
# print("total_time", strfdelta(tmdelta((time.perf_counter_ns() - prof.original_start_time)), '{mS} ms {µS} µs'))
