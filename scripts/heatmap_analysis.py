import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import csv
from matplotlib.image import NonUniformImage
from mpl_toolkits.axes_grid1 import make_axes_locatable


df = pd.read_csv('data/output_final_220526.csv')
print(df)
#data = pd.DataFrame.to_numpy(data)

x = df["coord_x"].to_numpy()
y = df["coord_y"].to_numpy()
print(x)

ax1 = df.plot.scatter(x='coord_x', y='coord_y')
plt.show()

heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
plt.imshow(heatmap.T, extent=extent, origin='lower',cmap="RdYlGn_r")
plt.show()






H, xedges, yedges = np.histogram2d(x, y, bins=30)
# Histogram does not follow Cartesian convention (see Notes),
# therefore transpose H for visualization purposes.
H = H.T

fig = plt.figure()

ax = fig.add_subplot(111, title='220526_phacelia-rapeseed',
        aspect='equal', xlim=(0,1), ylim=(0,1))


im = NonUniformImage(ax, interpolation='bilinear')
xcenters = (xedges[:-1] + xedges[1:]) / 2
ycenters = (yedges[:-1] + yedges[1:]) / 2
im.set_data(xcenters, ycenters, H)
ax.images.append(im)
ax.set_aspect(0.75)

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="4%", pad=0.1)

plt.colorbar(im, cax=cax)
plt.show()