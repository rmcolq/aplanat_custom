"""Plotting of spatial/3D data."""

from bokeh.models import ColorBar, LinearColorMapper, Range1d
from bokeh.palettes import Blues9
from bokeh.plotting import figure

from aplanat import util


def heatmap(x, y, z, name=None, **kwargs):
    """Create a heatmap from three columns.

    :param x: x-axis coordinates.
    :param y: y-axis coordinates.
    :param z: z-axis coordinates (e.g. counts or frequencies).
    :param name: title for z-axis.
    :param kwargs: kwargs for bokeh figure.

    :returns: a bokeh plot.

    """
    data = {'x': x, 'y': y, 'z': z}

    defaults = {
        "output_backend": "webgl",
        "height": 300, "width": 600}
    defaults.update(kwargs)
    p = figure(**defaults)

    # define a colour map
    colors = Blues9[::-1]
    mapper = LinearColorMapper(
        palette=colors, low=min(data['z']), high=max(data['z']))

    # plot heatmap rectangles
    p.rect(
        source=data, x="x", y="y", width=1, height=1,
        fill_color={'field': 'z', 'transform': mapper},
        line_color=None)

    # add colour scale
    color_bar = ColorBar(
        title=name, color_mapper=mapper, label_standoff=10,
        location=(0, 0))
    p.add_layout(color_bar, 'right')

    # hide some plotting artefacts
    p.x_range.range_padding = 0
    p.y_range.range_padding = 0
    p.xaxis.visible = False
    p.yaxis.visible = False
    # set up the axes
    xbounds = util.pad(data['x'])
    ybounds = util.pad(data['y'])
    p.x_range = Range1d(start=xbounds[0], end=xbounds[1], bounds=xbounds)
    p.y_range = Range1d(start=ybounds[0], end=ybounds[1], bounds=ybounds)
    return p
