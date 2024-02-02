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
import random
from pathlib import Path

import typing

from matplotlib import pyplot
from matplotlib.axes import Axes

from tools.plotting import Figure, ScatterPlot, _SubPlot, TSubPlot

fig = Figure(headless=False, rows=1)


def nltk_plot_style(ylabel: str, samples):
    def plot(ax: Axes):
        ax.grid(True, color="silver")
        ax.set_xticks(range(samples))
        # ax.set_xticklabels([str(s) for s in samples], rotation=90)
        ax.set_xlabel("Samples")
        ax.set_ylabel(ylabel)

    return plot


subplot: ScatterPlot = fig.subplot(title='test', style=nltk_plot_style('tst', 30), plot_type=ScatterPlot, index=0)
subplot.plot(x=[i for i in range(30)], y=[random.randrange(50, 100) for i in range(30)], s=[random.randrange(1, 100) for i in range(30)])
# subplot.plot([random.randrange(1, 100) for i in range(30)])
subplot.ax.legend(["Inline Label", 'Second Line'])
subplot.ax.set_xticks()

fig.figure.tight_layout()

fig.show()
# with Path('image.png').open('wb') as f:
#     f.write(fig.save())
