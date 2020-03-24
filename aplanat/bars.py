"""Creation of bar-like plots."""

from bokeh.models import Range1d
from bokeh.plotting import figure


def single_hbar(values, classes, colors, **kwargs):
    """Create a plot with a single set of stacked horizontal bars.

    :param values: values to stack.
    :param classes: names of items.
    :param colors: colours for each item.
    :param kwargs: kwargs for bokeh figure.

    :returns: a bokeh plot.

    After creating this plot, you may wish to change the following:

        * p.xaxis.axis_label: the axis label.
        * p.x_range: the x range of the plot.
    """
    if len(values) != len(classes) or len(values) != len(colors):
        raise ValueError(
            '`values`, `classes`, and `colors` must be of equal length.')

    # describe our data
    data = dict(zip(classes, values))

    defaults = {
        'y_range': [''],
        'plot_height': 150, 'plot_width': 600,
        'toolbar_location': None, 'tools': 'hover',
        'tooltips': '$name: @$name'}
    defaults.update(kwargs)

    # create the figure
    p = figure(**defaults)

    # plot horozontal bars
    p.hbar_stack(
        classes, y='y_value',
        height=0.9, alpha=0.7,
        color=colors, source=data,
        legend_label=classes)

    # hide some plotting artefacts
    p.xgrid.grid_line_color = None
    p.x_range = Range1d(0, int(1.2*sum(values)))
    p.yaxis.visible = False
    return p
