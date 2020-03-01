#This file is to be imported and run by other analysis
import pandas as pd
import numpy as np
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer, PorterStemmer
import re
#When the file is imported by another anlysis these instructions will show up
print("The function bi_dict_analysis is now available.\n"+
 " Pass in a data frame and the name of the dicionary (as string with .xlsx)"+
 " as arguments\n"+
"The dataframe 'df' should be limited to the rows you want to analyze\n"+
"Review text and title will be added in the reviews column\n"+
"words will be: lowered, stop words removed, punctuation and whitespace"+"
 removed\n"+
"Returns a tuple with the data frame with the added dictionary columns"+"
 first and column names second")
# ### Binary Dictionary Analysis
def bi_dict_analysis(df, dictio_filename):

    df['kindle'] = df['kindle'].astype(str)
    df.reset_index(inplace=True)
    df.drop(df.columns[0],axis=1,inplace=True)
    #Combine title and text
    df["reviews"] = df["title"].map(str) +" "+ df["text"]
    #Change the reviews type to string
    df['reviews'] = df['reviews'].astype(str)
    #Lowercase all reviews
    df.reviews = df.reviews.apply(lambda x: " ".join(x.lower() for x
                                                        in x.split()))
    #Remove punctuation
    df.reviews = df.reviews.str.replace('[^\w\s]','')
    #Remove stop words
    stop = stopwords.words('english')
    stop.remove("not")
    stop.remove("with")
    df.reviews = df.reviews.apply(lambda x: " ".join(x for x in x.split()
                                                        if x not in stop))
    # Import the dicionary for the analysis:
    dictio = pd.read_excel(r'C:\\Users\\...\\dicts\\'+dictio_filename)
    dictio = dictio.applymap(str)
    #Creates empty columns for the dictionaries
    column_names = []
    column_names = list(dictio.columns.values)
    df.reviews.dropna()
    #Saves all reviews in the sentences list
    sentences = df.reviews
    df= df.reindex(columns=[*df.columns.tolist(), *column_names],
                                                    fill_value=np.NaN)
    #Analysis starts
    i=0
    #Iterates through the reviews
    total_length = len(sentences)
    #Since the analysis can take very long, some status statements are printed
    print("Process started:")
    s = 1
    #Iteration through every review
    for sentence in sentences:
        #Splits a review text into single words
        words = sentence.split()
        previous_word = ""
        #Iterates through the topics, each is one column in a table
        for column in dictio:
            #Saves the topic words in the pattern list
            pattern = list(dictio[column])
            #Remove empty values
            clean_pattern = [x for x in pattern if str(x) != 'nan']
            match_score = 0
            #Iterates through each entry of the topic list
            for search_words in clean_pattern:
                #Iterates through each word of the review
                for word in words:
                    #When two consecutive words are searched for the first
                    #                           if statement gets activated
                    if len(search_words.split())>1:
                        pattern2 = r"( "+re.escape(search_words.split()[0])+
                        r"([a-z]+|) "+re.escape(search_words.split()[1])+
                                                            r"([a-z]+|))"
                        #The spaces are important so bedtime doesnt match time
                        if re.search(pattern2, " "+previous_word+" "+word,
                                                            re.IGNORECASE):
                            #If the word within the review matches the one
                            # in the dictionary the score is increased
                            match_score +=1
                    if len(search_words.split())==1:
                        pattern1 = r" "+re.escape(search_words)+r"([a-z]+|)"
                        if re.search(pattern1, " "+word, re.IGNORECASE):
                            match_score +=1
                    #Saves the word for the next iteration to be used as
                    # the previous word
                    #This enables to scan for two consecutive words
                    previous_word = word
            result=0
            #If one word in the review matched one word of the dictionary,
            # it is marked
            if match_score > 0:
                result = 1
            df.at[i, column] = int(result)
        i+=1
        #Prints current status
        factor = round(s/total_length,4)
        if factor%0.05 == 0:
            print("Status: "+str(factor*100)+"%")
        s+=1
    dictio_df = df.copy()
    print("Analysis successfull")
    return (dictio_df, column_names)
