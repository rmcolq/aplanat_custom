"""Histogram-like plots."""

from bokeh.models import Range1d
from bokeh.plotting import figure
import numpy as np

from aplanat.util import Limiter


def histogram(
        datas, weights=None, names=None, colors=None,
        normalize=False, bins=30, xlim=(None, None), ylim=(None, None),
        **kwargs):
    """Create a histogram plot.

    :param datas: a list of datasets, each item containing the data
        for that set.
    :params weights: a list of weight vectors (one for each dataset).
    :param names: the name of each dataset.
    :param colors: color used to plot each dataset.
    :param normalize: normalize histogram counts by total weight (across all
        datasets).
    :param bins: number of histogram bins.
    :param kwargs: kwargs for bokeh figure.

    :returns: a bokeh plot.

    After creating this plot, you may wish to change the following:

        * p.xaxis.axis_label
        * p.yaxis.axis_label
    """
    # TODO: slacken this
    if not isinstance(datas, list):
        raise ValueError(
            "datas and weights should be lists, one item per line to plot.")
    items = len(datas)
    if weights is None:
        weights = [None] * items
    if names is None:
        names = [None] * items
    if colors is None:
        colors = ['blue'] * items
    if any(len(x) != items for x in (weights, names, colors)):
        raise IndexError(
            "Lengths of datas, weights, names, and colors should be equal.")

    x_lim = Limiter()
    y_lim = Limiter()
    for data in datas:
        x_lim.accumulate(data)
    bins = np.linspace(x_lim.min, x_lim.max, num=bins)
    if normalize:
        total_weight = sum(sum(x) for x in weights)

    defaults = {
        "output_backend": "webgl",
        "height": 300, "width": 600}
    defaults.update(kwargs)

    p = figure(**defaults)
    for data, weight, name, color in zip(datas, weights, names, colors):
        counts, edges = np.histogram(data, weights=weight, bins=bins)
        if normalize:
            counts /= total_weight
        y_lim.accumulate(counts)
        kw = {}
        if name is not None:
            kw['legend_label'] = name
        if color is not None:
            kw['color'] = color
        p.quad(
            top=counts, bottom=0, left=edges[:-1], right=edges[1:],
            alpha=0.6, **kw)
    x_lim.fix(*xlim)
    y_lim.fix(*ylim)

    # limit the display range
    p.x_range = Range1d(
        start=x_lim.min, end=x_lim.max, bounds=(x_lim.min, x_lim.max))
    p.y_range = Range1d(
        start=y_lim.min, end=y_lim.max, bounds=(y_lim.min, y_lim.max))
    return p
