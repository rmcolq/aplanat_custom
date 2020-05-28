"""Report building from multiple items."""

from collections import OrderedDict
import uuid

from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.resources import INLINE
from jinja2 import Template
import markdown


class HTMLReport(OrderedDict):
    """Generate HTML Report from a series of bokeh figures.

    Items added to the report take an optional key argument, adding items
    with the same key allows an update in place whilst maintaining the order
    in which items were added.
    """

    def __init__(self, title="", lead=""):
        """Initialize the report item collection."""
        self.title = title
        self.lead = lead
        self.template = Template(
            """\
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>{{ title }}</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">

                    {{ resources }}
                    {{ script }}
                </head>
                <body>
            <div class="container">
              <h1>{{ title }}</h1>
              <p class="lead">{{ lead }}
            {{ div }}
                </body>
            </html>
            """  # noqa
        )
        self.plots = list()
        self.md = markdown.Markdown()

    def plot(self, plot, key=None):
        """Add a plot to the report.

        :param plot: bokeh plot instance.
        :param key: unique key for item.
        """
        if key is None:
            key = str(uuid.uuid4())
        self[key] = plot
        self.plots.append(key)

    def table(self, df, index=True, key=None, **kwargs):
        """Add a pandas dataframe to the report.

        :param df: pandas dataframe instance.
        :param index: include dataframe index in output.
        :param key: unique key for item.
        :param kwargs: passed to bokeh DataTable.
        """
        plot = bokeh_table(df, index=index, **kwargs)
        self.plot(plot, key)

    def markdown(self, text, key=None):
        """Add markdown formatted text to the report.

        :param text: markdown formatted text.
        :param key: unique key for item.
        """
        if key is None:
            key = str(uuid.uuid4())
        html = self.md.convert(text)
        self.md.reset()
        self[key] = html

    def render(self):
        """Generate HTML report containing figures."""
        resources = INLINE.render()
        plots = {k: self[k] for k in self.plots}
        script, plot_divs = components(plots)
        divs = list()
        for k in self.keys():
            try:
                divs.append(plot_divs[k])
            except KeyError:
                divs.append(self[k])
        divs = '\n'.join(divs)
        return self.template.render(
            title=self.title, lead=self.lead,
            resources=resources, script=script, div=divs)

    def write(self, path):
        """Write html report to file."""
        with open(path, "w", encoding='utf8') as outfile:
            outfile.write(self.render())


def bokeh_table(df, index=True, **kwargs):
    """Generate a bokeh table from a pandas dataframe."""
    columns = [TableColumn(field=x, title=x) for x in df.columns]
    if index:
        columns = [TableColumn(field="index", title="Feature")] + columns
    return DataTable(
            columns=columns, source=ColumnDataSource(df), index_position=None,
            **kwargs)
