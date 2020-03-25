"""Creation of line plots."""

from bokeh.models import Range1d
from bokeh.plotting import figure

from aplanat.util import Limiter


def line(
        x_datas, y_datas, names=None, colors=None,
        xlim=(None, None), ylim=(None, None),
        **kwargs):
    """Create a simple line plot.

    :param x_datas: a list of datasets, each item containing the
        data for that set.
    :params y_datas: a list of weight vectors (one for each dataset).
    :param names: the name of each dataset.
    :param colors: color used to plot each dataset.
    :param kwargs: kwargs for bokeh figure.

    :returns: a bokeh plot.

    After creating this plot, you may wish to change the following:

        * p.xaxis.axis_label
        * p.yaxis.axis_label
    """
    # TODO: slacken this
    if not isinstance(x_datas, list) or not isinstance(y_datas, list):
        raise ValueError(
            "x_datas and y_datas should be lists, one item per line to plot.")
    items = len(x_datas)
    if names is None:
        names = [None] * items
    if colors is None:
        colors = ['blue'] * items
    if any(len(x) != items for x in (y_datas, names, colors)):
        raise IndexError(
            "Lengths of x_datas, y_datas, names, and colors should be equal.")

    defaults = {
        "output_backend": "webgl",
        "height": 300, "width": 600}
    defaults.update(kwargs)

    p = figure(**defaults)
    x_lim = Limiter()
    y_lim = Limiter()
    for x, y, name, color in zip(x_datas, y_datas, names, colors):
        # TODO: add colours and names
        x_lim.accumulate(x)
        y_lim.accumulate(y)
        kw = {}
        if name is not None:
            kw['legend_label'] = name
        if color is not None:
            kw['color'] = color
        p.line(x=x, y=y, line_width=1.5, **kw)
    x_lim.fix(*xlim)
    y_lim.fix(*ylim)

    # limit the display range
    p.x_range = Range1d(
        start=x_lim.min, end=x_lim.max, bounds=(x_lim.min, x_lim.max))
    p.y_range = Range1d(
        start=y_lim.min, end=y_lim.max, bounds=(y_lim.min, y_lim.max))
    return p
