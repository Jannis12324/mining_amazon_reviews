import pandas as pd
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer, PorterStemmer
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob

print(("Function <make_senti_analysis> now available. Include the"+
    " following arguments: \n")+
     ("df: A data frame with a column <text> that is not cleaned yet \n")+
     ("Returns a data frame with the added column senti_score"))
#Only do once if needed (error will show in removing of stopwords when needed)
#nltk.download('stopwords')
def make_senti_analysis(df):
    #Lowercasing data
    #Change the reviews type to string
    df['text'] = df['text'].astype(str)
    #Lowercase all reviews
    df.text = df.text.apply(lambda x: " ".join(x.lower() for x in x.split()))
    #Remove punctuation
    df.text = df.text.str.replace('[^\w\s]','')
    #Remove stop words
    stop = stopwords.words('english')
    df.text = df.text.apply(lambda x: " ".join(x for x in x.split()
                                                            if x not in stop))
    #Stemming
    st = PorterStemmer()
    df.text = df.text.apply(lambda x: " ".join([st.stem(word)
                                                    for word in x.split()]))
    #Calculate sentiment analysis:
    def senti(x):
        return TextBlob(x).sentiment
    df['senti_score'] = df.text.apply(senti)
    df[['sentiment','subjectivity']] = pd.DataFrame(df['senti_score'].tolist(),
                                                                index=df.index)
    del df['senti_score']
    return df
