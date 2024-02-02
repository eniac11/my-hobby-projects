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
import difflib
import json
from imp import reload
from pprint import pprint
from typing import Optional

from server3 import main
from server3.StoryClassess import Sentence
from tools import semantic
from tools.htmls import transform, create_link, create_div


def get_class_with_id(id_, interable: list):
    for item in interable:
        if item.id == id_:
            return item


class EditorQuery:

    def __init__(self, data: dict):
        self.method = data['method']
        self.id = data['id']
        self.sentence = data['sentence']
        self.data = data


print(main.unpickled_story[0].children[0])


def run_query(query: EditorQuery):
    out = None
    if query.method == 'edit':
        sentence: Optional[Sentence] = None
        print(query.id)
        for chapter in main.unpickled_story:
            sentence: Sentence = get_class_with_id(query.id, chapter.internal_get_representation_blocks(Sentence))
            break
        sentence.add_change(query.sentence)
        out = sentence
    elif query.method == 'history':
        sentence: Optional[Sentence] = None
        for chapter in main.unpickled_story:
            sentence: Sentence = get_class_with_id(query.id, chapter.internal_get_representation_blocks(Sentence))
            break

        out = semantic.list_('divided', children=[
            semantic.item([semantic.content(children=[
                create_link('', inner=hist_sent, class_=['header']),
                create_div([datetime.datetime.fromtimestamp(timestamp).strftime('%I:%M:%S %p %d-%M-%Y')])
            ])]) for timestamp, hist_sent in sentence.history
        ])
    return out
# 9374b375-fbc1-43a2-981d-d68c3fb855f4
# 9374b375-fbc1-43a2-981d-d68c3fb855f4

# print(transform(main.unpickled_story[0].internal_get_representation_blocks(Sentence)[0]))
# q = EditorQuery({'method': 'edit', 'id': main.unpickled_story[0].internal_get_representation_blocks(Sentence)[0].id,'sentence': 'Looking back fd to the start of reality when the world suddenly  that a change, so  and impactful to future generations.'})
# run_query(q)
# print(transform(main.unpickled_story[0].internal_get_representation_blocks(Sentence)[0]))
# print(main.unpickled_story[0].internal_get_representation_blocks(Sentence)[0].history)
