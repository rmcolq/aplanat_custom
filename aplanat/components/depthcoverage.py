#!/usr/bin/env python
"""Create depth coverage report."""

import argparse

from bokeh.layouts import gridplot, layout
from bokeh.models import Panel, Tabs
import numpy as np
import pandas as pd

from aplanat import lines
from aplanat.report import _maybe_new_report, HTMLReport
from aplanat.util import Colors


_full_report_header = """
### Depth Coverage

The following tables and figures are derived from
the output of [Mosdepth]
(https://github.com/brentp/mosdepth).
"""


def cumulative_depth_from_dist(depth_file: str, **kwargs):
    """Cumulative depth plots from mosdepth dist file.

    param: depth_file: mosdepth.*.dist.txt file
    """
    df = pd.read_csv(
        depth_file, sep='\t', names=['ref', 'coverage', 'proportion'])
    df = df[df.ref == 'total']  # Use whole genome
    df.coverage = df['coverage'].astype(int)
    df.sort_values('coverage', ascending=True, inplace=True)
    p = lines.line(
        [df.coverage], [df.proportion],
        x_axis_label='Read depth',
        y_axis_label='Percentage of genome',
        **kwargs)
    return p


def cumulative_depth_from_bed(df: pd.DataFrame, bins: int = 100, **kwargs):
    """Cumulative depth plot from a mosdepth bed derived dataframe.

    :param df: depth dataframe
        Required columns:
        - start
        - end
        - depth
    :param: bins: number of bins for coverage
    :param: kwargs: keyword arguments for aplanat.lines.line
    """
    df.sort_values('depth', ascending=True, inplace=True)
    df['step'] = df.end - df.start
    df['cumsum_step'] = df.step.cumsum()
    x = df.depth.to_numpy()
    binner = len(x) // bins
    # Select slices from the depth-sorted array
    x = x[1:-1:binner]                  # Coverage
    y = np.array(list(range(len(x))))   # Proportion of genome
    # Normalise y to percentage of genome
    y = y / y[-1] * 100
    y = np.flip(y)
    p = lines.line(
        [x], [y],
        x_axis_label='Read depth',
        y_axis_label='Percentage of genome',
        **kwargs)
    return p


def depth_coverage(depth_file, xlim=(None, None), ylim=(None, None), **kwargs):
    """Create plot of depth coverage by region per ref name.

    :param depth_file: depth file output from mosdepth
    :param xlim: tuple for plotting limits (start, end). A value None will
        trigger calculation from the data.
    :param ylim: tuple for plotting limits (start, end). A value None will
        trigger calculation from the data.

    :returns: a list of bokeh plots.
    """
    depth_file = pd.read_csv(depth_file, sep='\t')
    depth_file.columns = ['ref', 'start', 'end', 'depth']
    all_ref = dict(tuple(depth_file.groupby(['ref'])))
    plots = []
    for ref in sorted(all_ref):
        depths = all_ref[ref]
        plot = lines.steps(
            list([depths['start']]), list([depths['depth']]),
            colors=[Colors.cerulean], mode='after',
            x_axis_label='Position along reference',
            y_axis_label='Sequencing depth / Bases',
            title=str(ref), xlim=xlim, ylim=ylim, **kwargs)
        plot.xaxis.formatter.use_scientific = False
        plots.append(plot)
    return plots


def depth_coverage_orientation(
        fwd, rev, xlim=(None, None), ylim=(None, None), **kwargs):
    """Create plot of depth coverage by region per ref name with fwd and rev.

    :param fwd: fwd depth file output from mosdepth
    :param rev: rev depth file output from mosdepth
    :param xlim: tuple for plotting limits (start, end). A value None will
        trigger calculation from the data.
    :param ylim: tuple for plotting limits (start, end). A value None will
        trigger calculation from the data.

    :returns: a list of bokeh plots.
    """
    depth_file = pd.read_csv(fwd, sep='\t')
    depth_file.columns = ['ref', 'start', 'end', 'fwd']
    rev_file = pd.read_csv(rev, sep='\t')
    rev_file.columns = ['ref', 'start', 'end', 'rev']
    depth_file['rev'] = rev_file['rev']
    all_ref = dict(tuple(depth_file.groupby(['ref'])))
    plots = []
    for ref in sorted(all_ref):
        depths = all_ref[ref]
        plot = lines.steps(
            [list(depths['start']), list(depths['start'])],
            [list(depths['fwd']), list(depths['rev'])],
            colors=[Colors.cerulean, Colors.feldgrau],
            names=['fwd', 'rev'], mode='after',
            x_axis_label='Position along reference',
            y_axis_label='Sequencing depth / Bases',
            title=str(ref), xlim=xlim, ylim=ylim, **kwargs)
        plot.xaxis.formatter.use_scientific = False
        plots.append(plot)
    return plots


def full_report(
        depth_file, fwd, rev, header=_full_report_header, report=None,
        sample_counts=False,
        tab=False, **kwargs):
    """Create a report section from the output of fastcat.

    :param depth_file: a depth file outout from mosdepth.
    :param fwd: fwd depth file output from mosdepth
    :param rev: rev depth file output from mosdepth
    :param header: a markdown formatted header.
    :param report: an HTMLSection instances
    :param tab: tabular output

    :returns: an HTMLSection instance, if `report`
        was provided the given instance is modified and returned.
    """
    report = _maybe_new_report(report)
    report.markdown(header)

    plots_coverage = depth_coverage(depth_file)
    plots_orient = depth_coverage_orientation(fwd, rev)

    if tab:
        tab1 = Panel(
                child=gridplot(plots_coverage, ncols=1),
                title="Proportions covered")
        tab2 = Panel(
                child=gridplot(plots_orient, ncols=1),
                title="Coverage traces")
        plots = Tabs(tabs=[tab1, tab2])
        report.plot(plots)
    else:
        plots = [[plots_coverage, plots_orient]]
        report.plot(layout(plots, sizing_mode="stretch_width"))
    return report


def main(args):
    """Entry point to create a report from depth file."""
    report = full_report(
        args.depth_file, args.fwd, args.rev, report=HTMLReport(),
        tab=args.tab)
    report.write(args.output)


def argparser():
    """Argument parser for entrypoint."""
    parser = argparse.ArgumentParser(
        "Depth coverage for one input file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False)
    parser.add_argument(
        "--depth_file",
        help="Mosdepth depth file.")
    parser.add_argument(
        "--fwd",
        help="Mosdepth fwd file.")
    parser.add_argument(
        "--rev",
        help="Mosdepth rev file.")
    parser.add_argument(
        "--tab", default=False,
        help="Tabular output")
    parser.add_argument(
        "--output", default="depth_coverage.html",
        help="Output HTML file.")

    return parser
