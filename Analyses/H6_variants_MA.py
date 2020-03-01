get_ipython().run_line_magic('matplotlib', 'notebook')
import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import os
from pandas import ExcelWriter
import re
# Loading the data
path = 'C:\\Users\\...\\All_reviews.csv'
df = pd.read_csv(path, dtype={"kindle":object})
df.drop(df.columns[0],axis=1, inplace=True)
figpath = 'C:\\Users\\...\\Pandas Figures\\'
# Defining kindle colors:
kindle_colors= ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c',
                                                '#fdbf6f','#cab2d6','#6a3d9a']
#Overview over all options
#Dropping all the rows that hold no information for the variant tree
af = df[(df["kindle"].isin(('3', '8', 'oasis 9', 'paperwhite 10',
                                            'paperwhite 6', 'voyage 7')))]
#Rename the options so they are uniform
af.connectivity = af.connectivity.replace('Only', '', regex = True)
af.connectivity = af.connectivity.replace('AT&T', 'Wi-Fi + Cellular',
                                                                regex = True)
af.connectivity = af.connectivity.replace('Connectivity', '', regex = True)
af.connectivity = af.connectivity.replace('Free', '', regex = True)
af["percent"] = 1
#Calculate percentage of each variant
temp = af.groupby(["kindle","connectivity","digital storage", "color"])
                                                    .agg({'percent': 'sum'})
pc = temp.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
#Overview over variants
ov = af.groupby(["kindle","connectivity","digital storage", "color"]).count()
pc["absolute"] = ov.id
#Prints tables with all variants
print(pc)
#Variant without "Na" rows
pc.drop(("3","Na","Na","Na" ), inplace=True)
pc.drop(("paperwhite 6", "Na","Na","Na"), inplace=True)
#Prints table of variant without Na rows
print(pc)
#Get the share of all colors
sf = df[(df["color"].isin(('Graphite', 'White', 'Black', 'Champagne Gold')))]
import re
def spec_of(string):
    with_spec = r"Champagne Gold"
    if re.search(with_spec , str(string), re.IGNORECASE):
        string = "Gold"
    return string
sf["color"] = sf["color"].astype(str)
sf["color"] = sf["color"].apply(spec_of)
sg=sf.groupby("color").describe()
sg.drop(sg.columns[1:],axis=1,inplace=True)
sort = sg.sort_values(sg.columns[0], ascending = False)
colors = sort.iloc[:,0]
color_labels = colors.index.values
colors = colors.values
print(color_labels)
#Get the share of Storage capacity and connectivity for all Kindles
af = df[(df["digital storage"].isin((' 2 GB', ' 4 GB', '8 GB', '32 GB')))]
af["digital storage"] = af["digital storage"].replace(' GB', '', regex = True)
af["digital storage"]=af["digital storage"].astype(int)
ag = af.groupby( "digital storage").describe()
ag.drop(ag.columns[1:],axis=1,inplace=True)
ag.index.sort
storage = ag.iloc[:,0]
storage_labels = storage.index.values
storage = storage.values
print(storage_labels)
#Get the share of the Connectivity for all Kindles
af = df.copy()
af.connectivity = af.connectivity.replace(' Only', '', regex = True)
af.connectivity = af.connectivity.replace('AT&T', ' Wi-Fi + Cellular',
                                                                regex = True)
af.connectivity = af.connectivity.replace('Connectivity', '', regex = True)
af.connectivity = af.connectivity.replace('Free', '', regex = True)
af.connectivity = af.connectivity.replace(' ', '', regex = True)
pf = af[(af["connectivity"].isin(('Wi-Fi', 'Wi-Fi+Cellular', 'Wi-Fi+Cellular',
                                                                    'Wi-Fi')))]
pg = pf.groupby("connectivity").describe()
pg.drop(pg.columns[1:],axis=1,inplace=True)
connectivity = pg.iloc[:,0]
connectivity_labels = connectivity.index.values
connectivity = connectivity.values
print(connectivity)
#Kindle unlimited
#Prints unique values of the Kindle unlimited option
print(df["kindle unlimited"].unique())
#Draws the graph that shows the share of options across all Kindles
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(9,4))
ax0, ax1, ax2 = axes.flatten()
axes = [ax0, ax1,ax2]
i=0
storage_labels=["2 Gb", "4 Gb", "8 Gb", "32 Gb"]
data = [colors, storage, connectivity]
labels = [color_labels, storage_labels, connectivity_labels]
legend = ["Colors", "Storage capacity", "Connectivity"]
N=1
ind = np.arange(N)
#Draws color stacked bar
black = ax0.bar(ind, colors[0], width, color = "Black")
graphite = ax0.bar(ind, colors[1], width, bottom = colors[0],
                                                        color = "darkgrey")
white = ax0.bar(ind, colors[2], width, bottom = colors[1]+colors[0],
                                                                color="snow")
gold = ax0.bar(ind, colors[3], width, bottom = colors[1]+colors[0]+colors[2],
                                                                color="gold")
ax0.legend((gold[0], white[0], graphite[0],black[0]), (color_labels[3],
            color_labels[2],color_labels[1],color_labels[0]),loc="lower right")
ax0.spines['top'].set_visible(False)
ax0.set_ylabel('Number of reviews', size = 12)
#Draws storage stacked bar
two = ax1.bar(ind, storage[0], width, color="Black")
four = ax1.bar(ind, storage[1], width, bottom = storage[0], color = "dimgrey")
eight = ax1.bar(ind, storage[2], width, bottom = storage[1]+storage[0],
                                                            color="darkgrey")
thirtytwo = ax1.bar(ind, storage[3], width, bottom = storage[1]+storage[0]
                                                +storage[2], color="lightgray")
ax1.legend((thirtytwo[0], eight[0], four[0],two[0]), (storage_labels[3],
    storage_labels[2],storage_labels[1],storage_labels[0]),loc="lower right")
#Draws connectivity stacked bar
wifi = ax2.bar(ind, connectivity[0], width, color="dimgrey")
cell = ax2.bar(ind, connectivity[1], width, bottom = connectivity[0],
                                                        color = "darkgrey")
ax2.legend((cell[0], wifi[0]), (connectivity_labels[1],connectivity_labels[0]),
                                                        loc="lower right")
i=0
for axis in axes:
    #Removes the axis and the boxes
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
    #Adds the titles
    axis.set_title(legend[i])
    i+=1
fig.tight_layout()
plt.savefig(figpath+"variant_three_stacked_bar",dpi=300)
plt.show()
#Removes the tick labels
for axis in axes:
    for label in axis.xaxis.get_ticklabels()[::]:
        label.set_visible(False)
