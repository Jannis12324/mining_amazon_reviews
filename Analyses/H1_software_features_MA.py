import pandas as pd
import numpy as np
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer, PorterStemmer
from wordcloud import STOPWORDS
import re
#Only do once if needed (error will show in removing of stopwords when needed)
#nltk.download('stopwords')
#Loading the data
path = 'C:\\Users\\...\\all_gr50.csv'
df = pd.read_csv(path, dtype={"kindle":object})
df.drop(df.columns[0],axis=1, inplace=True)
figpath = 'C:\\Users\\...\\Pandas Figures\\'
df['kindle'] = df['kindle'].astype(str)
#Drop all unneeded reviews
df = df[df['kindle'].isin(["paperwhite 7", "8", "oasis 9","paperwhite 10"])]#
df.reset_index(inplace=True, drop=True)
#Binary dictionary analysis
#Import the method
get_ipython().run_line_magic('run', 'function_bi_dict_analysis.ipynb')
#Run the analysis with the imported method
(da, column_names) = bi_dict_analysis(df,"Software_features_dict.xlsx")
#Count how often each dictionary got mentioned
rdf= da.copy()
grdf= rdf.groupby(["kindle"]).sum()
count = rdf.groupby(["kindle"]).count()
count.drop(count.columns[1:],axis=1,inplace=True)
grdf.drop(grdf.columns[0:3],axis=1,inplace=True)
results = grdf
latex = grdf.T
#Moving the paperwhite 7 column to the front for proper order
latex = latex[ ['paperwhite 7'] + [ col for col in latex.columns
                                                if col != 'paperwhite 7' ] ]
latex = latex.astype(int)
#Print results in a latex formatted way
print (latex.to_latex())
#Calculates how many times the topics were mentioned across the kindles
df = rdf
grdf= rdf.groupby(["kindle"]).sum()
count = rdf.groupby(["kindle"]).count()
count.drop(count.columns[1:],axis=1,inplace=True)
grdf.drop(grdf.columns[0:3],axis=1,inplace=True)
print(grdf.sum())
#Ratings dependend on discussed topic
#Calculates the mean rating whether the topic was discussed about or not
results = pd.DataFrame()
for column in column_names:
    zdf = rdf.groupby([column]).mean()
    zdf.drop(zdf.columns[1:], axis = 1, inplace = True)
    results[column] = zdf.stars
#Generates the table for the latex document
table = results.T
table["Num. of reviews"] = list(grdf.sum())
table["Num. of reviews"] = table["Num. of reviews"].astype(int)
table["change"] = round(table[1.0]-table[0.0],2)
table[1.0] = round(table[1.0],2)
table[0.0] = round(table[0.0],2)
table = table[["Num. of reviews", 1.0, 0.0, "change"]]
def redgreen(num):
    if num<0:
        return "\textcolor{DarkRed}{"+str(num)+"}"
    if num>0:
        return "\textcolor{Green}{"+str(num)+"}"
    else:
        return str(num)
table.change = table.change.apply(lambda x: redgreen(x))
print(table.to_latex(escape=False))
#Average rating across all reviews
print(rdf.stars.mean())
