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
import os

import requests

from controlling.main import ControlData

os.environ['NO_PROXY'] = '127.0.0.1'

#
# test_object({'test'})
# test_macro()
# test_object({'te'})
# test_macro()
# test_object(['h',7])
# test_macro()
#
# rt.testing()
#
# datas = list(ipc_handler.send())

controlData = ControlData('hello', data={'test': 'tset'})

# for data in datas:
resp = requests.post(url="http://127.0.0.1:5000", json=controlData.serialize())

