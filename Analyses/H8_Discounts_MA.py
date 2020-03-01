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
kindle_barplot = kindle_latex = {"3":"Kindle 3","4":"Kindle 4","5":"Kindle 5",
                "5 paperwhite":"Paperwhite 5", "6 paperwhite":"Paperwhite 6",
                "7": "Kindle 7", "7 paperwhite":"Paperwhite 7",
                "7 voyage":"Voyage","8":"Kindle 8","9 oasis":"Oasis",
                "99 paperwhite ten":"Paperwhite 10"}
#Rebate analysis
#Import the price history for the Kindle Paperwhite 10
prices = pd.read_excel(r'C:\\Users\\...\\pw10_8gb_spec_off_price history.xlsx')
#Import PW10 data
path = 'C:\\Users\\...\\All_reviews.csv'
df = pd.read_csv(path, dtype={"kindle":object})
df.drop(df.columns[0],axis=1, inplace=True)
#Filter for Paperwhite 10 reviews
df['kindle'] = df['kindle'].astype(str)
df = df[df['kindle'].isin(["paperwhite 10"])]
df.reset_index(inplace=True, drop=True)
#Filter for the 8GB option
df = df[(df["digital storage"]== "8 GB")]
#Filter for the Special offer option
df= df[df["offer type"]==' With Special Offers']
#Limit reviews to the dates of the price data
af =df[(df["date"]>"2018-11-16")& (df["date"]<"2019-08-22")]
af.sort_values(by=['date'], inplace=True, ascending=True)
#Run the dicionary analysis on the "return" dictionary
get_ipython().run_line_magic('run', 'func_bi_dict_analysis.ipynb')
(df, column_names) = bi_dict_analysis(af,"return_dict.xlsx" )
wdf = df.copy()
#Import and run the sentiment analysis
get_ipython().run_line_magic('run', 'func_senti_analysis.ipynb')
edf= make_senti_analysis(wdf)
#Transform the data in the wanted format
ret = edf.copy()
ret["reviews"] = 1
sent = edf.copy()
gret = ret.groupby("date").sum()
gsent = sent.groupby("date").mean()
gret["sent"] = gsent["sentiment"]
gret["bad"] = gret["Return"]
gret.drop(["sentiment", "comments", "subjectivity","Complaints","stars",
            "Return"], axis=1,inplace=True)
gret["stars"] = gsent["stars"]
gret["price"] = prices["Price"].values
#Calculate rolling mean for highly fluctual data
gret['rol_mean'] = gret['stars'].rolling(5).mean()
gret['rol_sent'] = gret['sent'].rolling(5).mean()
gret['rol_rev'] = gret['reviews'].rolling(5).mean()
gret['rol_ret'] = gret['bad'].rolling(5).mean()
#Makes sure that the graph is aligned by filling the missing
#values at the beginning
import math
gret['rol_mean'] = gret['rol_mean'].apply(lambda x: 4.1
                                            if math.isnan(x) else x)
gret['rol_sent'] = gret['rol_sent'].apply(lambda x: 0.22
                                            if math.isnan(x) else x)
gret['rol_rev'] = gret['rol_rev'].apply(lambda x: 25 if math.isnan(x) else x)
gret['rol_ret'] = gret['rol_sent'].apply(lambda x: 2 if math.isnan(x) else x)
gret["returned_perc"]= gret["rol_ret"]/gret["rol_rev"]
#Draw the graph
gret.index = pd.to_datetime(gret.index)
date = mpl.dates.date2num(gret.index.to_pydatetime())
retur = gret["bad"].values
price = gret["price"].values
stars = gret["rol_mean"].values
sent = gret["rol_sent"].values
reviews = gret["reviews"].values
t = date
objects = gret.index
y_pos = np.arange(len(objects))
fig, axs = plt.subplots(5,1,figsize=(16.5,10))
axs[0].bar(t, retur, align='center', color="gray")
axs[0].set_ylabel('Returns')
axs[0].grid(True)
axs[0].xaxis.set_major_locator(mdates.MonthLocator())
axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%B'))
axs[1].plot(t, stars, color="gray")
axs[1].set_ylabel('Avg. rating')
axs[1].grid(True)
axs[1].xaxis.set_major_locator(mdates.MonthLocator())
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%B'))
axs[2].plot(t, price, color="gray")
axs[2].set_ylabel('Price in [$]')
axs[2].grid(True)
axs[2].xaxis.set_major_locator(mdates.MonthLocator())
axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%B'))
axs[3].plot(t, sent, color="gray")
axs[3].set_ylabel('Avg. sentiment')
axs[3].grid(True)
axs[3].xaxis.set_major_locator(mdates.MonthLocator())
axs[3].xaxis.set_major_formatter(mdates.DateFormatter('%B'))
axs[4].bar(t, reviews, align="center", color="gray")
axs[4].set_xlabel('Reviews of 2018 and 2019')
axs[4].set_ylabel('Num. of reviews')
axs[4].grid(True)
axs[4].xaxis.set_major_locator(mdates.MonthLocator())
axs[4].xaxis.set_major_formatter(mdates.DateFormatter('%B'))
for i in range(4):
    for label in axs[i].xaxis.get_ticklabels()[::]:
        label.set_visible(False)
fig.tight_layout()
plt.savefig(figpath+"rebates.png",dpi=300)
plt.show()
