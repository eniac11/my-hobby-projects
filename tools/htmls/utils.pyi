from typing import Any, Callable, Iterable

from tools.htmls.html import Element

class Transform:
    def __init__(self, elem=None):
        self.elem_: Any = elem


    def __transform__(self): ...

    def replace(self, replacement): ...

class ListTransform(Transform): ...


class TextBlock(Transform): ...


def transform(transformer) -> Element: ...

class DelayedTransform(Transform):

    def __init__(self, elem, func: Callable):
        super().__init__(elem)
        self.func: Callable = func

def unpack(iterable: Iterable) -> Iterable: ...

def process_variable_underscore(val: str) -> str: ...

def equatify(d: dict[str, Any]) -> str: ...
