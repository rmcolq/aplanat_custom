"""Simple bokeh plotting API."""

import functools
import os

import bokeh.io as bkio
from bokeh.layouts import gridplot
from bokeh.model import Model, Range1d
from bokeh.models.annotations import Label
from bokeh.plotting import figure
import fontawesome.icons as fontawesome
from pkg_resources import resource_filename

__version__ = '0.0.4'


def with_fontawesome(f):
    """Decorate a plotting function ensuring font awesome is available.

    The function achieves two things: i) triggers the building of bokeh
    custom model which simply includes font awesome and ii) manipulates
    the current working directory to ensure when the extension build is
    triggered (by a call to bokeh.show) we are running somewhere that is
    writeable, otherwise node complains.
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        wd = os.getcwd()
        os.chdir(os.path.expanduser("~"))

        class LoadFontAwesome(Model):
            """Interpreting this will make the FontAwesome fonts available."""

            __implementation__ = resource_filename(
                "aplanat", "fontawesome_icon.ts")
            __dependencies__ = {"font-awesome": "^4.6.3"}

        f(*args, **kwargs)
        os.chdir(wd)
    return wrapper


class Grid(list):
    """Create a list of lists of fixed length."""

    def __init__(self, width=4):
        """Initialize the Grid."""
        self.width = width
        self.append(list())

    def add(self, item):
        """Add an item to the grid.

        :param item: item to add

        """
        self[-1].append(item)
        if len(self[-1]) == self.width:
            self.append(list())

    def extend(self, items):
        """Add multiple items.

        :param items: items to add.

        """
        for item in items:
            self.add(item)


def show(plot):
    """Show a plot in a notebook."""
    bkio.output_notebook(hide_banner=True)
    bkio.show(plot)


def grid(plots, ncol=4, **kwargs):
    """Show a grid of plots in a notebook.

    :param plots: a list of bokeh plots.
    :param ncol: number of columns.
    :param kwargs: kwargs for bokeh `gridplot`.

    """
    grid = Grid(width=ncol)
    grid.extend(plots)
    plot = gridplot(grid, **kwargs)
    show(plot)


@with_fontawesome
def infographic(items, ncol=4):
    """Create and infographic 'plot'.

    :param items: 3-tuples of (label, value, icon); the label should be
        a one or two word description, the value the headline number, and the
        icon the name of a fontawesome icon.
    :param ncol: number of columns in grid of items.

    """
    plots = list()
    for label, value, icon in items:
        p = figure(
            plot_width=175, plot_height=100,
            title=None, toolbar_location=None)
        p.axis.visible = False
        p.grid.visible = False
        p.outline_line_color = None
        p.rect([0.5], [0.5], [1.0], [1.0], fill_color="#2171b5")
        p.x_range = Range1d(start=0.1, end=0.9, bounds=(0.1, 0.9))
        p.y_range = Range1d(start=0.1, end=0.9, bounds=(0.1, 0.9))
        p.add_layout(
            Label(
                x=0.15, y=0.45, text=value, text_color="#DEEBF7",
                text_font_size="24px"))
        p.add_layout(
            Label(
                x=0.15, y=0.2, text=label, text_color="#C6DBEF",
                text_font_size="16px"))
        p.add_layout(
            Label(
                x=0.65, y=0.4, text=fontawesome[icon], text_color="#6BAED6",
                text_font="FontAwesome", text_font_size="48px"))
        plots.append(p)
    grid(plots, ncol=ncol, toolbar_location=None)
