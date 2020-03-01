get_ipython().run_line_magic('matplotlib', 'notebook')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
#Loading the data
path = 'C:\\Users\\...\\All_reviews.csv'
df = pd.read_csv(path, dtype={"kindle":object})
df.drop(df.columns[0],axis=1, inplace=True)
figpath = 'C:\\Users\\...\\Pandas Figures\\'
#Defining kindle colors:
kindle_colors= ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c',
                                                '#fdbf6f','#cab2d6','#6a3d9a']
#3x3 Multiplot of reviews over one year
a = df.groupby(["kindle","id","date"], sort=False).count()
data = pd.DataFrame(a["ASIN"])
#Define the year in which each Kindle has reviews in every month
years= ['2011-01-01','2011-12-31',
        '2012-01-01','2012-12-31',
        '2013-01-01','2013-12-31',
        '2013-01-01','2013-12-31',
        '2014-01-01','2014-12-31',
        '2016-01-01','2016-12-31',
        '2017-01-01','2017-12-31',
        '2017-01-01','2017-12-31',
        '2018-01-01','2018-12-31'
       ]
#Iterate through the kindles and apply the same operations
k3 = data.xs(key="3", level="kindle")
k4 = data.xs(key="4", level="kindle")
k5 = data.xs(key="5", level="kindle")
pw5 = data.xs(key="paperwhite 5", level="kindle")
pw6 = data.xs(key="paperwhite 6", level="kindle")
k7 = data.xs(key="7", level="kindle")
pw7 = data.xs(key="paperwhite 7", level="kindle")
k8 = data.xs(key="8", level="kindle")
o9 = data.xs(key="oasis 9", level="kindle")
i=0
y=0
kindles = [k3, k4,k5, pw5, pw6, k7,pw7, k8, o9]
for product in kindles:
    #Convert the data into the correct format for matplotlib
    product.reset_index(inplace=True)
    product.drop(product.columns[0],axis=1, inplace=True)
    product.set_index('date', inplace=True)
    product.index = pd.to_datetime(product.index)
    product = product.loc[years[y]:years[y+1]]
    product = mpl.dates.date2num(product.index.to_pydatetime())
    kindles[i] = product
    i+=1
    y+=2
#Results in a list of arrays with the dates of review releases: kindles
#Create the plot with matplotlib
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(12,10))
ax0, ax1, ax2, ax3, ax4, ax5, ax7, ax8, ax9 = axes.flatten()
axes = [ax0, ax1, ax2, ax3, ax4, ax5, ax7, ax8, ax9]
i=0
review_year = ["2011", "2012", "2013", "2013", "2014", "2016","2017",
                "2017", "2018"]
legend = ["Kindle 3", "Kindle 4", "Kindle 5", "Paperwhite 5",
               "Paperwhite 6", "Kindle 7","Paperwhite 7", "Kindle 8", "Oasis 9"]
bins = 24
size = 12
for axis in axes:
    axis.hist(kindles[i], bins, histtype='bar', color=kindle_colors[i])
    #axis.legend(prop={'size': size})
    axis.set_title(legend[i]+", reviews of "+review_year[i])
    axis.xaxis.set_major_locator(mdates.MonthLocator())
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%m'))
    #axis.get_legend().remove()
    i+=1
fig.tight_layout()
plt.savefig(figpath+"9panelreviews_per_kindle_oneyear.png",dpi=300)
plt.show()
#Histogram for all reviews over the month
#Extract how many reviews per Kindle were published per day
a = df.groupby(["kindle","id","date"], sort=False).count()
data = pd.DataFrame(a["ASIN"])
#Iterate through the kindles and apply the same operations
k3 = data.xs(key="3", level="kindle")
k4 = data.xs(key="4", level="kindle")
k5 = data.xs(key="5", level="kindle")
pw5 = data.xs(key="paperwhite 5", level="kindle")
pw6 = data.xs(key="paperwhite 6", level="kindle")
k7 = data.xs(key="7", level="kindle")
pw7 = data.xs(key="paperwhite 7", level="kindle")
k8 = data.xs(key="8", level="kindle")
o9 = data.xs(key="oasis 9", level="kindle")
i=0
kindles = [k3, k4,k5, pw5, pw6, k7, pw7, k8, o9]
#Remove the year of all dates to map all reviews over one year
def changeyear(date):
    year = "2000-"
    new_date =year+ date[5:]
    return new_date
for product in kindles:
    #Convert the data into the correct format for matplotlib
    #and remove the year from the date
    product.reset_index(inplace=True)
    product.drop(product.columns[0],axis=1, inplace=True)
    product.date = product["date"].apply(changeyear)
    product.set_index('date', inplace=True)
    product.index = pd.to_datetime(product.index)
    product = mpl.dates.date2num(product.index.to_pydatetime())
    kindles[i] = product
    i+=1
#Sketch the plot
legend = ["Kindle 3", "Kindle 4", "Kindle 5", "Paperwhite 5",
               "Paperwhite 6", "Kindle 7", "Paperwhite 7",
                "Kindle 8", "Oasis 9"]
fig = plt.figure(figsize=(12,6))
s = fig.add_subplot(111)
#Data needs to be an array to work
s.hist(kindles,bins=52,stacked=True, color=kindle_colors, alpha=1)
s.xaxis.set_major_locator(mdates.MonthLocator())
s.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
plt.xticks(rotation=45, size = 12)
s.legend(legend)
plt.savefig(figpath+"num_of_reviews_months.png",dpi=300, bbox_inches = "tight")
#Binary dictionary analysis with vacation dictionary
get_ipython().run_line_magic('run', 'function_bi_dict_analysis.ipynb')
(df, column_names) = bi_dict_analysis(df,"vacation_dict.xlsx")
#Print KPIs for all reviews that mention vacation
vac = df[df.Vacation == 1.0]
print(vac.describe())
#Kindle colors without Voyage and Paperwhite 10
kindle_colors= ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c',
                '#fdbf6f','#cab2d6','#6a3d9a']
#Gets number of reviews per day for each Kindle
a = vac.groupby(["kindle","id","date"], sort=False).count()
data = pd.DataFrame(a["ASIN"])
#Iterate through the kindles and apply the same operations
k3 = data.xs(key="3", level="kindle")
k4 = data.xs(key="4", level="kindle")
k5 = data.xs(key="5", level="kindle")
pw5 = data.xs(key="paperwhite 5", level="kindle")
pw6 = data.xs(key="paperwhite 6", level="kindle")
k7 = data.xs(key="7", level="kindle")
pw7 = data.xs(key="paperwhite 7", level="kindle")
k8 = data.xs(key="8", level="kindle")
o9 = data.xs(key="oasis 9", level="kindle")
i=0
kindles = [k3, k4,k5, pw5, pw6, k7, pw7, k8, o9]
#Maps the reviews over the months
def changeyear(date):
    year = "2000-"
    new_date =year+ date[5:]
    return new_date
#Prepares the data of each Kindle for the graph
for product in kindles:
    #Convert the data into the correct format for matplotlib and remove
    #the year from the date
    product.reset_index(inplace=True)
    product.drop(product.columns[0],axis=1, inplace=True)
    product.date = product["date"].apply(changeyear)
    product.set_index('date', inplace=True)
    product.index = pd.to_datetime(product.index)
    product = mpl.dates.date2num(product.index.to_pydatetime())
    kindles[i] = product
    i+=1
#Draws a graph that with the reviews mentioning vacations per week
legend = ["Kindle 3", "Kindle 4", "Kindle 5", "Paperwhite 5",
               "Paperwhite 6", "Kindle 7", "Paperwhite 7",
                "Kindle 8", "Oasis 9"]
fig = plt.figure(figsize=(12,6))
s = fig.add_subplot(111)
#Data needs to be an array to work
s.hist(kindles,bins=52,stacked=True, color=kindle_colors, alpha=1)
s.xaxis.set_major_locator(mdates.MonthLocator())
s.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
plt.xticks(rotation=45)
s.legend(legend)
plt.savefig(figpath+"num_vacation_dict_oneyear.png",dpi=300,
                                                bbox_inches = "tight")
#Normalize the number of reviews per week
#Convert to datetime
ddf = df
vac['date'] =  pd.to_datetime(vac['date'])
ddf["date"] = pd.to_datetime(ddf["date"])
#Extract the week out of the date
vac['week'] = vac['date'].dt.week
ddf["week"] = ddf["date"].dt.week
#Create a data frame with both: number of dict hits per week and number
#of total reviews per week
weekvac = vac.groupby(["week"], sort=True).count()
agg = pd.DataFrame(weekvac["id"])
weekddf = ddf.groupby(["week"],sort = True).count()
agg["total_reviews"] = weekddf.ASIN
agg["normed"] = (agg.id/agg.total_reviews)*100
#Draws a graph of normed vacation dict hits per week
fig = plt.figure(figsize=(14,8))
b = fig.add_subplot(111)
#Create the normed bar chart
objects = agg.index
y_pos = np.arange(len(objects))
performance = agg.normed
b.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
for label in b.xaxis.get_ticklabels()[1::2]:
    label.set_visible(False)
plt.ylabel('Percentage of vacation hits per week')
plt.title('Week')
plt.savefig(figpath+"normed_vacation_dict.png",dpi=300, bbox_inches = "tight")
plt.show()
