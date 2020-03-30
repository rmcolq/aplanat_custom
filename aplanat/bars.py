"""Creation of bar-like plots."""

from bokeh.models import Range1d
from bokeh.plotting import figure
import pandas as pd

from aplanat import util


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
    data = dict(zip(classes, ([x] for x in values)))
    data['y_value'] = ['']

    defaults = {
        'output_backend': 'webgl',
        'y_range': data['y_value'],
        'plot_height': 150, 'plot_width': 600,
        'toolbar_location': None, 'tools': 'hover',
        'tooltips': '$name: @$name'}
    defaults.update(kwargs)

    p = figure(**defaults)
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


def boxplot_series(
        groups, values, xlim=(None, None), ylim=(None, None),
        **kwargs):
    """Create a (e.g. time-) series of boxplots for a variable.

    :param groups: the grouping variable (the x-axis values).
    :param values: the data for boxplots are drawn (the y-axis values).
    :param xlim: tuple for plotting limits (start, end). A value None will
        trigger calculation from the data.
    :param ylim: tuple for plotting limits (start, end). A value None will
        trigger calculation from the data.
    :param kwargs: kwargs for bokeh figure.

    :returns: a bokeh plot.

    After creating this plot, you may wish to change the following:

        * p.xaxis.axis_label = 'Read Length / bases'
        * p.yaxis.axis_label = 'Number of reads'
    """
    df = pd.DataFrame(dict(
       group=groups, value=values))
    uniq = df.group.unique()

    # find the quartiles and IQR for each category
    groups = df.groupby('group')
    quantiles = groups.quantile([0.25, 0.5, 0.75])
    quantiles.index.names = ['group', 'quantile']
    q1 = quantiles.xs(0.25, level='quantile')
    q2 = quantiles.xs(0.50, level='quantile')
    q3 = quantiles.xs(0.75, level='quantile')
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr

    defaults = {
        "output_backend": "webgl",
        "height": 300, "width": 600}
    defaults.update(kwargs)
    p = figure(**defaults)

    # stems
    p.segment(uniq, upper.value, uniq, q3.value, line_color="black")
    p.segment(uniq, lower.value, uniq, q1.value, line_color="black")

    # boxes
    for low, high in ((q2.value, q3.value), (q1.value, q2.value)):
        p.vbar(
            uniq, 0.8, low, high,
            fill_color="blue", alpha=0.7,
            line_color="black")

    # set up the axes
    xlim = util.Limiter(util.pad(uniq)).fix(*xlim)
    ylim = util.Limiter().accumulate(df['value']).fix(*ylim)
    p.x_range = Range1d(
        start=xlim.min, end=xlim.max, bounds=(xlim.min, xlim.max))
    p.y_range = Range1d(
        start=ylim.min, end=ylim.max, bounds=(ylim.min, ylim.max))
    return p
