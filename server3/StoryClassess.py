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
import uuid

from tools.htmls import *
from tools.htmls.html import ElementTransform
from tools.htmls.layout import *

from server3 import styles


class Chapter(ElementTransform):
    format_spec = "Chapter {no}: {title}"
    chapters = 1

    def __init__(self, title, children):
        super().__init__()
        self.title = title
        self.children = children
        self.link_ = InternalLink(create_header(self.format(), level=3))
        Chapter.chapters += 1

    def __transform__(self):
        return create_element('section', children=[
            self.link_,
            create_div(self.children)
        ])

    def page_view(self):
        return [
            center(self.link_),
            create_div(self.children)
        ]

    def format(self):
        return self.format_spec.format(no=self.chapters, title=self.title)

    def link(self):
        return self.link_.link(self.format())


class Sentence(Transform):

    def __init__(self, text:str):
        super().__init__(TextBlock(text))
        self.id = str(uuid.uuid4())
        self.history = [(time.time(), text)]
        self.current = 0

    def get_current(self):
        return self.history[self.current][1]

    def add_change(self, text):
        self.current += 1
        self.history.append((time.time(), text))
        print(self.history)

    def __transform__(self):
        return create_element('span', inner=TextBlock(self.get_current()), id_=self.id, class_=[styles.edit()])
