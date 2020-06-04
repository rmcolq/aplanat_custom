import numpy as np
import pandas as pd

import aplanat
from aplanat import bio, hist, points, report, spatial

x = np.random.normal(size=2000)
y = np.random.normal(size=2000)
sorted_xy = [np.sort(x), np.sort(x)]

# Start a report
report = report.HTMLReport(
    "Aplanat Demo", "A demonstration of aplanat and its report generation API",
    require_keys = False)  # set True to require keys on item addition

# The report is an ordered dictionary, so we can add placeholders to
# delay the addition of items. Markdown can be used for text items.
report.markdown("placeholder", key="simple preamble")

# Adding a plot
report.plot(points.points(sorted_xy, sorted_xy[::-1]), key="line_plot")

# Using placeholder is more explicit, and checks will be made before
# rendering that the item has be assigned a real value
report.placeholder("histogram preamble")

# There's no need to provide key (unless require_keys is set). Items added
# without a key cannot be replaced however.
report.plot(hist.histogram([x, y], colors=['red', 'green']))

# To delete an item, just delete the key
report.markdown("Garbage", key='garbage')
del report['garbage']

# Add more plots
report.placeholder("heatmap preamble")
report.plot(spatial.heatmap2(x, y))

# Add a data table
report.placeholder("table preamble")
df = pd.DataFrame({'x':x, 'y':y})
report.table(df, index=False)
report.markdown(
    "Small tables have their `height` manipulated to shrink by default."
    "This can be overridden with `shrink=False`.")
df = df[0:5]
report.table(df, key='Table with auto_height', height=200)

# Gallery
report.placeholder("gallery preamble")
exec_summary = aplanat.InfoGraphItems()
exec_summary.append('Total reads', 1000000, 'angle-up', '')
exec_summary.append('Total yield', 1e9, 'signal', 'b')
exec_summary.append('Mean read length', 50e3, 'align-center', 'b')
exec_summary.append('Mean qscore (pass)', 14, 'thumbs-up', '')
plot = aplanat.infographic(exec_summary.values(), ncols=2)
report.plot(plot)

chroms = np.random.choice(bio.chrom_data['chrom'], size=10000)
positions = list()
for chrom in chroms:
    length = bio.chrom_data.loc[bio.chrom_data['chrom'] == chrom, 'length']
    positions.append(np.random.randint(length)[0])
plot = bio.karyotype([positions], [chroms])
report.plot(plot)

# Trying to render now will raise ValueError because the placeholders are
# not filled in
try:
    report.render()
except ValueError as e:
    print("Caught error as expected:", e)

# Fill in the placeholders
report.markdown("""
### Simple plots

A simple line plot:
""", "simple preamble")

report.markdown("""
### Histograms

Multi-variate histograms:
""", "histogram preamble")

report.markdown("""
### Heatmaps

Heatmaps from `x-y` values:
""", "heatmap preamble")

report.markdown("""
### Tables

Data tables:
""", "table preamble")


report.markdown("""
### Gallery

Assortment of possibilities:
""", "gallery preamble")

# write the output, implicitely calls .render()
report.write("demo.html")
