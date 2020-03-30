"""Simple bokeh plotting API."""

import bokeh.io as bkio


__version__ = '0.0.2'


def show(plot):
    """Show a plot in a notebook."""
    bkio.output_notebook(hide_banner=True)
    bkio.show(plot)
