"""Report building from multiple items."""

from collections import OrderedDict
import uuid

from bokeh.embed import components
from bokeh.model import Model
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.resources import INLINE
from jinja2 import Template
import markdown


class HTMLSection(OrderedDict):
    """A section of a report.

    The class can be extended o provide novel report components by
    overriding `._extra_components()`.
    """

    def __init__(self, require_keys=False):
        """Initialize the report item collection.

        :param title: report title.
        :param lead: report strapline, shown below title.
        :param require_keys: require keys when adding items.
        """
        self.require_keys = require_keys
        self.plots = list()
        self.md = markdown.Markdown()

    def _add_item(self, item, key=None):
        """Add an item to the report.

        :param item: item to add.
        :param key: unique key for item.
        """
        if key is None:
            if self.require_keys:
                raise ValueError('A key is required.')
            else:
                key = str(uuid.uuid4())
        self[key] = item

    def placeholder(self, key):
        """Add a placeholder to be filled in later."""
        self._add_item(None, key=key)

    def plot(self, plot, key=None):
        """Add a plot to the report.

        :param plot: bokeh plot instance.
        :param key: unique key for item.
        """
        self._add_item(plot, key=key)

    def table(self, df, index=True, key=None, shrink=True, **kwargs):
        """Add a pandas dataframe to the report.

        :param df: pandas dataframe instance.
        :param index: include dataframe index in output.
        :param key: unique key for item.
        :param shrink: shrink wrap the table to avoid whitespace.
        :param kwargs: passed to bokeh DataTable.
        """
        plot = bokeh_table(df, index=index, **kwargs)
        plot.height = min(plot.height, 25*(len(df) + 1))
        self.plot(plot, key)

    def markdown(self, text, key=None):
        """Add markdown formatted text to the report.

        :param text: markdown formatted text.
        :param key: unique key for item.
        """
        if text is None or text == '':
            return
        html = self.md.convert(text)
        self.md.reset()
        self._add_item(html, key=key)

    def _plot_components(self):
        """Return html script and div tags for bokeh plots."""
        # handle bokeh plots
        scripts = list()
        divs = dict()
        plots = {k: v for k, v in self.items() if isinstance(v, Model)}
        if len(plots) > 0:
            scripts, divs = components(plots)
            scripts = [scripts]
        return scripts, divs

    def _table_components(self):
        """Return html script and div for tables."""
        # TODO: reimplement `.table()` to not use bokeh?
        pass

    def _extra_components(self):
        """Return additional script and divs."""
        # hook for derived classes:
        # return: list of scripts, dict of divs keyed on self.keys
        return list(), dict()

    def components(self):
        """Fetch script and div tags for report."""
        scripts = list()
        specials = dict()
        # retrieve bokeh plot divs
        plot_scripts, plot_divs = self._plot_components()
        scripts.extend(plot_scripts)
        specials.update(plot_divs)
        # TODO: add special handing for new tables?
        # retrieve any extra specials
        extra_scripts, extra_divs = self._extra_components()
        scripts.extend(extra_scripts)
        specials.update(extra_divs)

        # put things together in order
        divs = list()
        for k in self.keys():
            try:
                divs.append(specials[k])
            except KeyError:
                if self[k] is None:
                    raise ValueError(
                        "Placeholder `{}` was not assigned "
                        "a value.".format(k)
                        )
                # fall back to putting items in directly
                divs.append(self[k])
        return scripts, divs


class HTMLReport(HTMLSection):
    """Generate HTML Report from a series of bokeh figures.

    Items added to the report take an optional key argument, adding items
    with the same key allows an update in place whilst maintaining the order
    in which items were added. Items can be grouped into sections for easier
    out of order addition.
    """

    def __init__(self, title="", lead="", require_keys=False):
        """Initialize the report item collection.

        :param title: report title.
        :param lead: report strapline, shown below title.
        :param require_keys: require keys when adding items.
        """
        super().__init__(require_keys=require_keys)
        self.title = title
        self.lead = lead
        self.sections = OrderedDict()
        self.sections['main'] = self
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

    def add_section(self, key=None, section=None):
        """Add a section (grouping of items) to the report.

        :param key: unique key for section.
        :param section: `HTMLSection` to add rather than creating anew.

        :returns: the report section.

        """
        if key is None:
            key = str(uuid.uuid4())
        if section is None:
            section = HTMLSection(require_keys=self.require_keys)
        else:
            if not isinstance(section, HTMLSection):
                raise TypeError("`section` should be an `HTMLSection`.")
        self.sections[key] = section
        return self.sections[key]

    def render(self):
        """Generate HTML report containing figures."""
        resources = INLINE.render()

        all_scripts = list()
        all_divs = list()
        for sec_name, section in self.sections.items():
            scripts, divs = section.components()
            all_scripts.extend(scripts)
            all_divs.extend(divs)

        script = '\n'.join(all_scripts)
        divs = '\n'.join(all_divs)
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
