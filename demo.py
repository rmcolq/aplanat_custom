import numpy as np

from aplanat import hist, lines, report, spatial

x = np.random.normal(size=200)
y = np.random.normal(size=200)
sorted_xy = [np.sort(x), np.sort(x)]

report = report.HTMLReport(
    "Aplanat Demo", "A demonstration of aplanat and its report generation API")

report.markdown("placeholder", "simple preamble")
report.plot(lines.line(sorted_xy, sorted_xy[::-1]), 'line_plot')
report.markdown("placeholder", "histogram preamble")
report.plot(hist.histogram([x, y], colors=['red', 'green']))  # no need == no replacement
report.markdown("placeholder", "heatmap preamble")
report.plot(spatial.heatmap2(x, y))

# adding again keeps things in the same place
report.markdown("""
Simple plots
------------

A simple line plot
""", 'simple preamble')

report.markdown("""
Histograms
----------

Histograms
""", 'histogram preamble')


report.markdown("""
Heatmaps
--------

Heatmaps
""", 'heatmap preamble')

# write the output
report.write("demo.html")

