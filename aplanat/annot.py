"""Add annotations to plots."""

from bokeh.models import Span, Title
import numpy as np


def marker_vline(plot, x, label=None, color='black', width=1.5):
    """Add a vertical line to a plot with optional label.

    :param plot: a bokeh plot instance.
    :param x: the x-axis value where the line should be added.
    :param label: text label.
    :param color: colour for line.
    :param width: line width.

    :returns: updated plot.

    """
    ymax = plot.y_range.end
    vline = Span(
        location=x, dimension='height',
        line_color=color, line_width=width)
    plot.renderers.extend([vline])
    if label is not None:
        plot.text(
            x=[x], y=[0.5 * ymax], angle=np.pi / 2, text=[label])
    return plot


def subtitle(plot, subtitle):
    """Add a subtitle to a plot.

    :param subtitle: the title to add

    :returns: updated plot.
    """
    plot.add_layout(
        Title(text=subtitle, text_font_style='italic'), 'above')
    return plot
