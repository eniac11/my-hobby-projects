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
from __future__ import annotations

from enum import Enum
from typing import Optional, Type

from tools.htmls.html_elements import *
from tools.htmls.utils import *

__all__ = ["ContentTypes", "CodeLine", 'CodeBlock', 'InlineCodeBlock', 'quote', 'Function', 'FunctionCall', 'Script',
           'create_script', 'Variable', 'MappedClass']


class ContentTypes(Enum):
    JSON = "application/json"


class CodeLine:

    def __init__(self, code: str, inline=False):
        self.code = code
        self.inline = inline

    def __str__(self):
        if not self.code.endswith(';') and not self.inline:
            return self.code + ";"
        return self.code


class CodeBlock:
    def __init__(self, lines: list[CodeLine]):
        self.code_lines: list[CodeLine] = lines
        for i, line in enumerate(self.code_lines):
            if issubclass(line.__class__, Transform):
                self.code_lines[i] = transform(line)
        # print(*self.code_lines)

    def __str__(self):
        return ''.join(map(str, self.code_lines))


class InlineCodeBlock(CodeBlock):

    def __init__(self, lines: list[CodeLine | Type[Transform]]):
        super().__init__(lines)
        for line in self.code_lines:
            line.inline = True

    def __str__(self):
        return ''.join(map(str, self.code_lines))


def quote(iterable: list):
    for i, val in enumerate(iterable):
        iterable[i] = "'" + str(val) + "'"
    return iterable


class FunctionCall:

    def __init__(self, function: Function, param: list[str], no_quote: bool = False):
        self.function = function
        self.params = param
        self.no_quote = no_quote

    def call(self, inline: bool = False):
        if self.no_quote:
            code = f"""{self.function.name}({', '.join(map(str, self.params))})"""
        else:
            code = f"""{self.function.name}({', '.join(quote(list(map(str, self.params))))})"""
        if inline:
            return CodeLine(code, True)
        return CodeLine(code)


class Function:

    def __init__(self, name: str, params: list[str], code: list[CodeBlock]):
        self.name = name
        self.code = code
        self.params = params

    def to_code(self):
        return InlineCodeBlock([
            CodeLine(f"function {self.name}({', '.join(self.params)}) {{{''.join(map(str, self.code))}}}")
        ])

    def get_function_object(self):
        return self.name

    def __call__(self, params: list, no_quote: bool = False):
        return FunctionCall(self, params, no_quote)


class Script:

    def __init__(self, functions: list[Function]):
        super().__init__()
        self.functions = functions

    def __str__(self):
        return '\n'.join(map(str, map(lambda x: x.to_code(), self.functions)))


class Variable(Transform):

    def __init__(self, name, rhs):
        self.name = name
        self.rhs = rhs
        super().__init__(self.create())

    def set(self, rhs):
        self.rhs = rhs
        return CodeLine(f"{self.name} = {self.rhs}")

    def get(self):
        return CodeLine(self.name, True)

    def create(self):
        return CodeLine(f"let {self.name} = {self.rhs}")


class MappedClass:

    def __init__(self, name, mapped_functions: dict[str, dict]):
        self.name = name
        self.mapped_function = mapped_functions

    def __getattr__(self, item) -> Function:
        if (test := self.__dict__.get(item, None)) is not None:
            return test
        if item in self.mapped_function:
            func = Function(f'{self.name}.{item}', [], [])
            return func
        raise AttributeError(f'{self.__class__.__name__}.{item} not found.')

    def __call__(self, *args, **kwargs):
        return MappedClass(self.name, self.mapped_function[self.name])

    def call(self, inline: bool = False):
        if self.no_quote:
            code = f"""{self.function.name}({', '.join(map(str, self.params))})"""
        else:
            code = f"""{self.function.name}({', '.join(quote(list(map(str, self.params))))})"""
        if inline:
            return CodeLine(code, True)
        return CodeLine(code)


class MappedClassCall():

    def __init__(self, parent: MappedClass, name, param: list[str], no_quote: bool = False):
        self.parent = parent
        self.params = param
        self.no_quote = no_quote

    def call(self, inline: bool = False):
        if self.no_quote:
            code = f"""{self.function.name}({', '.join(map(str, self.params))})"""
        else:
            code = f"""{self.function.name}({', '.join(quote(list(map(str, self.params))))})"""
        if inline:
            return CodeLine(code, True)
        return CodeLine(code)


def create_script(*, url=None, defer=False, script: Optional[Script] = None, **kwargs):
    elem_kwargs = {}
    if defer:
        elem_kwargs['defer'] = True
    if url is None:
        elem_kwargs['inner'] = script
    else:
        elem_kwargs['src'] = url
    kwargs.update(elem_kwargs)
    return create_element('script', **kwargs)
