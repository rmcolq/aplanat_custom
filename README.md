Aplanat
=======

Aplanat provides a wrappers (templates) around the bokeh library to simplify
the plotting of common plots, with a particular focus on producing plots in
Juypyter notebook environments.

Installation
------------

Aplanat is easily installed in the standard python tradition:

    git clone --recursive https://github.com/epi2me-labs/aplanat.git
    cd aplanat
    pip install -r requirements.txt
    python setup.py install

or via pip:

    pip install aplanat.


Usage
-----

Aplanat does not try to be everything to everyone; this is both the power
and downfall of a number of plotting libraries. Being overly generic leads
to confusing documentation and boilerplate code. As much as the developers
love the declarative nature of `ggplot` in `R`, aplanat eschews this approach
in search of something more transparent --- aplanat does not try to be too
clever with your data.

Rather aplanat attempts to make constructing common plots as simple as possible
by translating directly a users inputs into displayed data. Most plotting
functions are of the form:

    plot = plot_function(
        [series_1_x, series_2_x, ...], [series_1_y, series_2_y, ...],
        name=[series_1_name, series_2_name, ...],
        colors=[series_1_color, series_1_color, ...])

Here are some examples, plotting a kernel density estimate (a simple line plot
having computed the transform of the data):

    import aplanat
    from aplanat import lines, util
    data = [....]  # a list or numpy array
    x_grid, pdf = util.kernel_density_estimate(data)
    plot = lines.line([x_grid], [pdf])
    aplanat.show(plot)  # to show the plot in a notebook

To add axis and plot titles:

    plot = lines.line(...,
       title='Chart title', x_axis_label='x-axis', y_axis_label='y-axis')

To plot multiple series just extend the lists given to the arguments (this
time using points):

    from aplanat import points
    x0, y0 = [...], [...]
    x1, y1 = [...], [...]
    plot = points.points([x0, x1], [y0, y1])

Plotting a histogram:

    from aplanat import hist
    data = [...]   # a list or numpy array
    plot = hist.histogram([data], bins=400)

A simple bar plot illustrating counts of groups:

    groups = [...]
    counts = [...]
    plot = bars.simple_bar(groups, counts)

A set of boxplots illustrating how the distribution of variable changes (y-axis)
with a second grouping variable (the x-axis):

    from aplanat import bars
    values = [...] 
    groups = [...]  # as long as `values`, indicating the group for each value
    plot = bars.boxplot_series(groups, values)

Plot a heat map using a hexagonal binning (as seems to be popular these days):

    from aplanat import spatial
    x_values = [...]
    y_values = [...]
    plot = spatial.hexmap(x_values, y_values)

To show multiple plots, use `aplanat.grid` rather than `aplanat.show`:

    plots = [hist.histogram(x) for x in (...)]
    aplanat.grid(plots, ncol=3)

The plots will be shown filling a grid row-wise.
