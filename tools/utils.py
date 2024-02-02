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
import math
from string import Formatter


def clamp(value, min_, max_):
    return max(min(value, max_), min_)


def interpolate_value(value, from_min, from_max, to_min, to_max):
    # Figure out how 'wide' each range is
    from_span = from_max - from_min
    to_span = to_max - to_min

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - from_min) / float(from_span)

    # Convert the 0-1 range into a value in the right range.
    return to_min + (valueScaled * to_span)


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

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])