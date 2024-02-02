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
import pickle
import uuid
from pathlib import Path

import nltk.tokenize

from server3 import story
from server3.StoryClassess import Chapter, Sentence
from tools.htmls import TextBlock, create_p


def save_story():
    chapters = []
    for chapter in story.chapters:
        paragraphs = []
        for paragraph in chapter.get_elements_by_name('p'):
            text = ''.join(map(lambda x: x.elem_, paragraph.internal_get_representation_blocks(TextBlock)))
            sentences = []
            for sent in nltk.tokenize.sent_tokenize(text):
                sentences.append(Sentence(sent))
            paragraphs.append(create_p(children=sentences))
        chapters.append(Chapter(chapter.title, paragraphs))
    with Path('story.pickle').open('wb') as f:
        pickle.dump(chapters, f)


save_story()
