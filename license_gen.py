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
from pathlib import Path
import os

notice = """Copyright (C) 2024 Hadley Epstein

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

notice_lines = ('"""' + notice + '"""\n').splitlines(keepends=True)

for dirname, dirnames, filenames in os.walk(Path("."), topdown=True):
    if "__pycache__" in dirnames:
        dirnames.remove("__pycache__")

    for filename in filenames[::]:
        filename_ = Path(filename)
        if filename_.suffix != ".py":
            filenames.remove(filename)
            continue
    for filename in filenames:
        if filename in ["peewee.py", "pyjack.py", "bottle.py", "markdown2.py"]:
            continue
        with (Path(dirname) / filename).open("r+") as f:
            lines = f.readlines()
            l = notice_lines + lines
            f.seek(0)
            #print(l)
            f.writelines(l)

        
    #print(dirname, filenames)
