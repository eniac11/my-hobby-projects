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
import typing
from typing import Callable, Optional, Iterable, Any, Generic, TypeVar
import io

import abc

import matplotlib.figure
from matplotlib import pyplot
from matplotlib.axes import Axes
import matplotlib.collections
import matplotlib.lines
from matplotlib import rcParams
from numpy import ndarray

from tools.htmls import ElementTransform, create_image, Transform

TSubPlot = TypeVar("TSubPlot", bound='_SubPlot')
rcParams['svg.fonttype'] = 'none'


class _SubPlot(abc.ABC):

    def __init__(self, ax: Axes, title: str = '', style: Optional[Callable[[Axes], None]] = lambda ax_: None):
        self.ax = ax  # type:Axes
        self.title = title
        self.style = style
        self.style(self.ax)
        self.legend = self.ax.legend

    @abc.abstractmethod
    def plot(self, *args, **kwargs) -> matplotlib.collections.Collection:
        pass

    @property
    def title(self):
        return self.ax.get_title()

    @title.setter
    def title(self, value):
        self.ax.set_title(value)

    @property
    def ylabel(self) -> str:
        return self.ax.get_ylabel()

    @ylabel.setter
    def ylabel(self, value: str):
        self.ax.set_ylabel(value)

    @property
    def xlabel(self) -> str:
        return self.ax.get_xlabel()

    @xlabel.setter
    def xlabel(self, value: str):
        self.ax.set_xlabel(value)

    def xticks(self, labels: list[str], rotation: Optional[int] = None):
        if rotation is not None:
            self.ax.xaxis.set_ticks(range(len(labels)), labels, rotation=rotation)
        else:
            self.ax.xaxis.set_ticks(range(len(labels)), labels)


class LinePlot(_SubPlot):

    def __init__(self, ax: Axes, title: str = '', style: Optional[Callable[[Axes], None]] = lambda ax_: None):
        super().__init__(ax, title, style)

    def plot(self, *args, scalex=True, scaley=True, data=None, **kwargs) -> list[matplotlib.lines.Line2D]:
        return self.ax.plot(*args, scalex=True, scaley=True, data=None, **kwargs)


class BoxPlot(_SubPlot):

    def __init__(self, ax: Axes, title: str = '', style: Optional[Callable[[Axes], None]] = lambda ax_: None):
        super().__init__(ax, title, style)

    def plot(self, x: Any, notch: bool = None, sym: str | None = None, vert: bool = None, whis: Any = None,
             positions: ndarray | Iterable | int | float | None = None, widths: float | ndarray | Iterable | int = None,
             patch_artist: bool = None, bootstrap: int | None = None, usermedians: int | None = None,
             conf_intervals: ndarray | Iterable | int | float | None = None, meanline: bool = None,
             showmeans: Any = None, showcaps: Any = None, showbox: Any = None, showfliers: Any = None,
             boxprops: Any = None, labels: Iterable | None = None, flierprops: Any = None, medianprops: Any = None,
             meanprops: Any = None, capprops: Any = None, whiskerprops: Any = None, manage_ticks: bool = True,
             autorange: bool = False, zorder: float = None, capwidths: Any = None):
        return self.ax.boxplot(x, notch, sym, vert, whis, positions, widths, patch_artist, bootstrap, usermedians,
                               conf_intervals, meanline, showmeans, showcaps, showbox, showfliers, boxprops, labels,
                               flierprops, medianprops, meanprops, capprops, whiskerprops, manage_ticks, autorange,
                               zorder, capwidths)


class ScatterPlot(_SubPlot):

    def __init__(self, ax: Axes, title: str = '', style: Optional[Callable[[Axes], None]] = lambda ax_: None):
        super().__init__(ax, title, style)
        self.plot = self.ax.scatter

    def plot(self, x: float | ndarray | Iterable | int, y: float | ndarray | Iterable | int,
             s: float | ndarray | Iterable | int | None = None, c: ndarray | Iterable | int | float | None = None,
             marker: Any = None, cmap: Any = None, norm: Any = None, vmin: Any = None, vmax: Any = None,
             alpha: float = None, linewidths: Optional[float | ndarray | Iterable | int] = None, *,
             edgecolors: str = None, plotnonfinite: bool = False,
             **kwargs: Any) -> matplotlib.collections.PathCollection:
        return self.ax.scatter(x, y, s, c, marker, cmap, norm, vmin, vmax, alpha, linewidths, edgecolors, plotnonfinite,
                               **kwargs)


class Figure:

    def __init__(self, rows=1, cols=1, headless=False):
        super().__init__()
        self.headless = headless
        if not headless:
            self.figure: matplotlib.figure.Figure = pyplot.figure()
        else:
            self.figure: matplotlib.figure.Figure = matplotlib.figure.Figure()
        self.rows = rows
        self.cols = cols
        self._subplot_index = 0

    def save(self, format='png') -> str | bytes:
        match format:
            case 'png' | 'pdf':
                buf = io.BytesIO()
            case 'svg' | 'eps' | 'ps':
                buf = io.StringIO()
        self.figure.savefig(buf, format=format)
        buf.seek(0)
        return buf.getvalue()

    def show(self):
        self.figure.show()
        if not self.headless:
            pyplot.show()

    def set_size_in_cm(self, width: int, height: int):
        self.figure.set_size_inches(width / 2.54, height / 2.54)

    def _check_subplot_bounds(self):
        if self._subplot_index > self.rows * self.cols:
            raise Exception(f'Cannot add subplot Out of Bounds (max_subplots={self.rows*self.cols} have {self._subplot_index})')

    def subplot(self, title: str = '', style: Optional[Callable[[Axes], None]] = lambda ax_: None,
                plot_type: typing.Type[TSubPlot] = LinePlot, index: int = None) -> TSubPlot:
        if index is None:
            self._subplot_index += 1
            index = self._subplot_index
            self._check_subplot_bounds()
        else:
            index = index + 1
        ax = self.figure.add_subplot(self.rows, self.cols, index)
        return plot_type(ax, title, style)

# def lazy_figure(func):
#     def wrapper():
#         def fig(figure: Figure):
#             func(figure)
#
#         return fig
#
#     return wrapper()
#
#
# def sub_plot(func: Callable[[Axes], None], plot_style=None):
#     @lazy_figure
#     def wrapper(figure: Figure):
#         ax = figure.add_subplot(plot_style=plot_style)
#         func(ax)
#
#     return wrapper
#
#
# def create_figure(sub_plots: list[Callable]):
#     figure = Figure()
#     for sub_plot_ in sub_plots:
#         sub_plot_(figure)
#     return figure
