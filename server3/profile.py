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
import codecs
import urllib
import urllib.parse
import webbrowser

import pyinstrument
import pyinstrument_flame
import tempfile

with pyinstrument.Profiler() as profiler:
    from server3 import main

    p = str(main.page)

renderer = pyinstrument.profiler.renderers.HTMLRenderer()
renderer.open_in_browser(profiler.last_session)
renderer2 = pyinstrument_flame.FlameGraphRenderer(title="Task profile", flamechart=True)
svg = profiler.output(renderer)
# profiler.open_in_browser()

output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
output_filename = output_file.name
with codecs.getwriter("utf-8")(output_file) as f:
    f.write(profiler.output(renderer2))

url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
webbrowser.open(url)

# profiler.open_in_browser(True)
