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
from functools import partial

__all__ = ['transform_text', 'title', 'upper', 'bold', 'italic', 'underline', 'hr']

from tools.htmls.html import *
from tools.htmls.html import DelayedElementTransform, Element_Constructor
from tools.htmls.utils import *




def transform_text(elem: Element_Constructor | TextBlock | str, func):
    transformer = elem

    if type(transformer) in [TextBlock, str]:
        transformer = transform_block_to_text_block(elem)
        transformer.elem_ = func(transformer.elem_)
    if type(transformer) == Element_Constructor:
        text_blocks = transformer.internal_get_representation_blocks(TextBlock)

        for text_block in text_blocks:
            text_block.elem_ = func(text_block.elem_)
    return transformer


def title(elem):
    transformer = copy.deepcopy(elem)

    return DelayedElementTransform(transformer, partial(transform_text, func=str.title))


def upper(elem):
    transformer = copy.deepcopy(elem)
    return DelayedElementTransform(transformer, partial(transform_text, func=str.upper))


def bold(inner, **kwargs):
    return Element_Constructor('b', inner=inner, **kwargs)


def italic(inner, **kwargs):
    return Element_Constructor('i', inner=inner, **kwargs)


def underline(inner, **kwargs):
    return Element_Constructor('u', inner=inner, **kwargs)


def hr():
    return Element_Constructor('hr', single=True)
