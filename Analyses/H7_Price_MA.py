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
                '#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#fcfc05']
#Different dictionaries for reindexing if necessary
kindle_latex = {"3":"\keyboard{}","4":"\genfour{}","5":"\genfive{}",
                "5 paperwhite":"\pwgenfive{}", "6 paperwhite":"\pwgensix{}",
                "7": "\genseven{}", "7 paperwhite":"\pwgenseven{}",
                "7 voyage":"\voyage{}","8":"\geneight{}","9 oasis":"\oasis{}",
                "99 paperwhite ten":"\pwgenten{}"}
kindle_barplot = kindle_latex = {"3":"Kindle 3","4":"Kindle 4","5":"Kindle 5",
                "5 paperwhite":"Paperwhite 5", "6 paperwhite":"Paperwhite 6",
                "7": "Kindle 7", "7 paperwhite":"Paperwhite 7",
                "7 voyage":"Voyage","8":"Kindle 8","9 oasis":"Oasis",
                "99 paperwhite ten":"Paperwhite 10"}
#Dictionary Analysis for reviews that talk about the price
get_ipython().run_line_magic('run', 'func_bi_dict_analysis.ipynb')
(df, column_names) = bi_dict_analysis(df, "price_dict.xlsx")
wdf = df.copy()
wdf["total"]=1
#Changing Kindle names for alphabetical sorting
def rename(string):
    if string == "oasis 9":
        string = "9 oasis"
    if string == "paperwhite 10":
        string = "99 paperwhite ten"
    if string == "voyage 7":
        string = "7 voyage"
    if string == "paperwhite 5":
        string = "5 paperwhite"
    if string == "paperwhite 6":
        string = "6 paperwhite"
    if string == "paperwhite 7":
        string = "7 paperwhite"
    return string

wdf.kindle = wdf.kindle.apply(rename)
gdf = wdf.groupby("kindle").sum()
#Percentage of review that talk about a topic
gdf.drop(gdf.columns[0:1], axis=1, inplace=True)
gdf["price perc"] = 100*(gdf["price"])/(gdf["total"])
gdf["exp perc"] = 100*(gdf["expensive"])/(gdf["total"])
gdf["cheap perc"] = 100*(gdf["cheap"])/(gdf["total"])
#Reindex with predefined dictionary
gdf.rename(index=kindle_barplot,inplace=True)
#Drop unneccessary columns
gdf.drop(gdf.columns[0:4], axis =1, inplace=True)
bdf = gdf.copy()
#Print the table of expensive, cheap and price mentions
print(bdf)
#Draws the graph that compares how often the topics are mentioned
#for each Kindle
price = list(bdf["price perc"])
exp = list(bdf["exp perc"])
cheap = list(bdf["cheap perc"])
ind = np.arange(len(price))
width = 0.2
fig, ax = plt.subplots(figsize=(10,5))
ax2 = ax.twinx()
rects1 = ax.bar(ind-(width), price, width, label="Price", color="lightgrey")
rects11 = ax.bar(ind, exp, width, label="Expensive", color="lightcoral")
rects111= ax.bar(ind+(width), cheap, width, label="Cheap",color="lightgreen")
rects2 = ax2.bar(ind, exp, width, label="Expensive", color="lightcoral")
rects3 = ax2.bar(ind+(width), cheap, width, label="Cheap",color="lightgreen")
ax.set_ylabel("Price mentions per Kindle [%]", size=12)
ax2.set_ylabel("Cheap/Expensive mentions per Kindle [%]", size=12)
ax.set_xticks(ind)
ax.set_xticklabels(bdf.index.values,rotation=45, size = 12)
ax.legend()
fig.tight_layout()
plt.savefig(figpath+"price_mentions_per_kindle.png",dpi=300,
                                                    bbox_inches = "tight")
plt.show()
#Analyse average rating and sentiment depending if price is mentioned per Kindle
pdf = df.copy()
get_ipython().run_line_magic('run', 'func_senti_analysis.ipynb')
adf = make_senti_analysis(pdf)
edf = adf.copy()
edf.kindle = edf.kindle.apply(rename)
#Calculates absolute and percent of mentions
result = pd.DataFrame(columns=["kindle", "sone", "szero","schange","sentone",
                                "sentzero","sentchange"])
i=0
for kindle in edf["kindle"].unique():
    fdf = edf[(edf["kindle"]== kindle) & (edf["price"]==1)]
    starone = fdf["stars"].mean()
    result.at[i, "sone"] = round(starone,2)
    result.at[i, "kindle"] = kindle
    fdf = edf[(edf["kindle"]== kindle) & (edf["price"]==0)]
    starzero = fdf["stars"].mean()
    result.at[i, "szero"] = round(starzero,2)
    fdf = edf[(edf["kindle"]== kindle) & (edf["price"]==1)]
    sentone = fdf["sentiment"].mean()
    result.at[i, "sentone"] =round(sentone,2)
    fdf = edf[(edf["kindle"]== kindle) & (edf["price"]==0)]
    sentzero = fdf["sentiment"].mean()
    result.at[i, "sentzero"] = round(sentzero,2)
    i+=1
result["schange"] = result["sone"]-result["szero"]
result["sentchange"] = result["sentone"]-result["sentzero"]
result.set_index("kindle", inplace=True)
kindle_latex = {"3":"\keyboard{}","4":"\genfour{}","5":"\genfive{}",
                "5 paperwhite":"\pwgenfive{}", "6 paperwhite":"\pwgensix{}",
                "7": "\genseven{}", "7 paperwhite":"\pwgenseven{}",
                "7 voyage":"\voyage{}","8":"\geneight{}","9 oasis":"\oasis{}",
                "99 paperwhite ten":"\pwgenten{}"}
result.rename(index=kindle_latex,inplace=True)
