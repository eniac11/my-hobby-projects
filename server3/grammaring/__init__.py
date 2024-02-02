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
from typing import Generator, Iterable

import tools.language_tool as language_tool

from nltk.tokenize import sent_tokenize

from tools import semantic
from tools.htmls import *
import os

os.environ["NO_PROXY"] = "127.0.0.1"

tool = language_tool.LanguageTool(remote_address='http://127.0.0.1:8081')

import server3.story as story


def language_check(paragraph: Element) -> Iterable[tuple[str, list[language_tool.Match]]]:
    text_blocks = paragraph.internal_get_representation_blocks(TextBlock)
    test = ''.join(map(lambda x: x.elem_, text_blocks))
    sentences = sent_tokenize(test)
    for sentence in sentences:
        yield sentence, tool.check(sentence)


# print(story.chapters[0].elem.get_elements_by_element_name('p')[2].get_elements_by_element_name("u"))
popups = []


def style_underline(sentence: str, match: language_tool.Match, popup: Element):
    sentence_section = sentence[match.offset:match.offset + match.length]
    if match.rule.issue == "style":
        return underline(sentence_section, data=popup.get_id(),
                         class_=[semantic.styles.error(), semantic.styles.yellow()])
    if match.rule.issue == "grammar" or match.rule.issue == "typographical":
        return underline(sentence_section, data=popup.get_id(),
                         class_=[semantic.styles.error(), semantic.styles.green()])
    if match.rule.issue == "duplication":
        return underline(sentence_section, data=popup.get_id(),
                         class_=[semantic.styles.error(), semantic.styles.orange()])
    if match.contextForSureMatch < 1:
        return underline(sentence_section, data=popup.get_id(),
                         class_=[semantic.styles.error(), semantic.styles.red()])
    return underline(sentence_section, data=popup.get_id(),
                     class_=[semantic.styles.error()])


def check():
    popups.clear()
    paragraphs: list[Element] = transform(story.chapters[0]).get_elements_by_name('p')
    ps = []
    elements = []
    # text_blocks: list[TextBlock] = chapter.internal_get_representation_blocks(TextBlock)
    previous_offset = 0

    for paragraph in paragraphs:

        for sentence, matches in language_check(paragraph):
            matches_ = 0
            previous_offset = 0
            # print(sentence)
            # if len(matches) == 0:
            #     elements.append(TextBlock(sentence))
            #     continue
            for match in matches:
                popup = semantic.ui(children=[
                    create_div([
                        create_header(match.shortMessage, class_=["ui", "sub", "huge", "header"]),
                        create_element("span", inner=match.message)
                    ], class_=["header"]),
                    semantic.create_divider(),
                    semantic.stackable(create_div([
                        semantic.column([
                            semantic.item(
                                [
                                    semantic.button(
                                        children=[replacement], class_=["primary"]
                                    ) for replacement in match.replacements
                                ], class_=[semantic.styles.spaced()]),
                        ]),
                        semantic.column([
                            semantic.item(["Issue: ", match.rule.issue]),
                            semantic.item(["Rule: ", match.rule.id]),
                        ])

                    ], class_=["content"]))
                ], class_=["flowing", "popup"])
                under_line = style_underline(sentence, match, popup)
                elements.append(sentence[previous_offset:match.offset])
                elements.append(under_line)
                popups.append(popup)
                previous_offset = match.offset + match.length
                matches_ += 1
            if matches_ == 0:
                elements.append(sentence + " ")
                continue
            elements.append(sentence[previous_offset:-1] + sentence[-1] + " ")
            # print(repr(sentence))
        yield create_p(children=elements.copy())
        elements.clear()
