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
# Loading the data
path = 'C:\\Users\\...\\All_reviews.csv'
df = pd.read_csv(path, dtype={"kindle":object})
df.drop(df.columns[0],axis=1, inplace=True)
# Defining kindle colors:
kindle_colors= ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c',
                                            '#fdbf6f','#cab2d6','#6a3d9a']
figpath = 'C://Users//...//Pandas Figures//'
sf = df[(df["offer type"].isin((' Without Special Offers $159',
       ' Kindle with Special Offers', ' With Special Offers $139',
       'With Special Offers', 'Without Special Offers',
       ' With Special Offers', ' Without Special Offers')))]
#Enters a "1" if special offers are present
import re
def spec_of(string):
    with_spec = r"(With\s|with\s)"
    if re.search(with_spec , str(string), re.IGNORECASE):
        string = 1
    else:
        string = 0
    return string
sf["offer type"] = sf["offer type"].astype(str)
sf["offer"] = sf["offer type"].apply(spec_of)
#Checks whether conversion was successfull
sf["offer"].unique()
#Makes sure the else statement filtered out correctly
zero = sf[sf["offer"]==0]
zero["offer type"].unique()
del sf["offer type"]
#Imports and runs the sentiment analysis
get_ipython().run_line_magic('run', 'func_senti_analysis.ipynb')
sf = make_senti_analysis(sf)
#Prints the KPIs of the reviews grouped by special offer
print(sf.groupby("offer").describe())
print(sf.groupby("offer").count())
#Renames Kindles for correct alphabetical sorting
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
    return string
sf.kindle = sf.kindle.apply(rename)
#Displays the statistic for every Kindle based on whether
#they have special offer
gf = sf.groupby(["kindle", "offer"]).count()
print(gf)
#Calculates the normed values for the stacked bar graph and puts
# them in seperated lists
x=0
i=0
z=0
o=0
results=[0]*20
zero=[0]*10
one = [0]*10
values = list(gf.id.values)
for i in range(20):
    if i %2 == 0:
        x = values[i]/(values[i]+values[i+1])
        zero[z]=x
        z+=1
    if i %2 == 1:
        x = values[i]/(values[i]+values[i-1])
        one[o]=x
        o+=1
    results[i]=x
    i+=1
gf.drop(gf.columns[1:],axis = 1, inplace=True)
#Saves the result in the "percentage" column
gf["percentage"] = results
#Legend entries
kindles = ["Kindle 3", "Kindle 4", "Kindle 5", "Paperwhite 5",
           "Paperwhite 6", "Kindle 7", "Voyage", "Kindle 8",
          "Oasis", "Paperwhite 10"]
#Draws plot of shares of each Kindle with or without special offers
import numpy as np
import matplotlib.pyplot as plt
N = 10
without_off = zero
with_off = one
plt.figure(figsize=(10,5))
ind = np.arange(N)    # the x locations for the groups
width = 0.5       # the width of the bars: can also be len(x) sequence
p1 = plt.bar(ind, without_off, width, color="dimgrey")
p2 = plt.bar(ind, with_off, width, bottom=without_off,color="silver")
plt.ylabel('Share of Reviews',size=12)
plt.xticks(ind, kindles)
plt.legend((p2[0], p1[0]), ('With special offers', 'Without special offers'))
plt.xticks(rotation=45, size = 12)
plt.yticks(size = 10)
plt.savefig(figpath+"distribution_kindles_spec_off.png",dpi=300,
                                                bbox_inches = "tight")
plt.show()
#Analysis what the customers say about having special offers
offers = sf[sf["offer"]==1]
get_ipython().run_line_magic('run', 'func_bi_dict_analysis.ipynb')
(odf, column_names = bi_dict_analysis(offers, "special_offers_dict.xlsx")
wdf= odf.copy()
#What is the difference in rating when owners of kindles with special
#offers talk about the special offers vs. the reviews where they dont?
wdf.groupby("special_offers").mean()
#How many reviews comment on the special offers?
gwdf=wdf.groupby("special_offers").sum()
gwdf["percent"] = gwdf.offer.apply(lambda x: x/(gwdf.offer.sum()))
#Conduct a sentiment analysis
wdf = make_senti_analysis(wdf)
wdf.groupby("special_offers").sentiment.describe()
#Filter out all reviews with special offers
wc = wdf[wdf["special_offers"]==1]
get_ipython().run_line_magic('run', 'func_word_cloud.ipynb')
stopwords=["kindle", "book", "paperwhite", "amazon"]
make_wordcloud(wc, stopwords, "special_offer_wordcloud.png")
#Save to a file and do a topic analysis with the respective file
filename ="spec_of_reviews"
#Delete file if it exists
if os.path.isfile(filename):
    os.remove(filename)
wc.to_csv('C:\\Users\\...\\'+filename+".csv")
writer = ExcelWriter('C:\\Users\\...\\'+filename+".xlsx")
wc.to_excel(writer)
writer.save()
#Imports and runs a topic analysis on all reviews with special offers
get_ipython().run_line_magic('run', 'func_topic_analysis.ipynb')
make_topic_analysis(wc,10,stopwords)
get_ipython().run_line_magic('run', 'func_senti_analysis.ipynb')
swc = make_senti_analysis(wc)
swc.sentiment.min()
