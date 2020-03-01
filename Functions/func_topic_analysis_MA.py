import spacy
spacy.load('en')
from spacy.lang.en import English
import pandas as pd
parser = English()

print(("Function <make_topic_analysis> now available. Include the following"+
    " arguments: \n")+
     ("df: A data frame with a column <text> that is not cleaned yet \n")+
     ("NUM_TOPICS: The number of topics you want to end up with \n")+
     ("stopwords: A list of words that should not be included in the analysis")+
     ("if an error is thrown about english stopwords, execute the following"+
     " code before calling the fuction:\n")+
     ("nltk.download('stopwords'). Same goes for nltk.download('wordnet')"))
def make_topic_analysis(df, NUM_TOPICS, stopwords):
    #Remove digits
    df.text = df.text.replace('\d+', '', regex = True)
    #Remove punctuation, symbols and whitespace
    df.text = df.text.replace('[^\w\s\+]', '', regex = True)
    #Count the number of words of each review text
    df['count_text'] = df.text.apply(lambda x: len(str(x).split(' ')))
    #Count the number of words of each review title
    df['count_title'] = df.title.apply(lambda x: len(str(x).split(' ')))
    #Combine text count
    df["total"] = df.count_text + df.count_title
    #Only include reviews with more than 40 words
    df.loc[df.total < 40,"ov50"] = '0'
    df = df.drop(df[df.total < 40].index)
    #Delete the counting columns, as they are no longer needed
    del df["count_text"]
    del df["count_title"]
    del df["total"]
    #Tokenize text to form bag of words
    parser = English()
    def tokenize(text):
        lda_tokens = []
        tokens = parser(text)
        for token in tokens:
            if token.orth_.isspace():
                continue
            elif token.like_url:
                lda_tokens.append('URL')
            elif token.orth_.startswith('@'):
                lda_tokens.append('SCREEN_NAME')
            else:
                lda_tokens.append(token.lower_)
        return lda_tokens
    #Lemmatize text
    import nltk
    from nltk.corpus import wordnet as wn
    def get_lemma(word):
        lemma = wn.morphy(word)
        if lemma is None:
            return word
        else:
            return lemma
    from nltk.stem.wordnet import WordNetLemmatizer
    def get_lemma2(word):
        return WordNetLemmatizer().lemmatize(word)
    #Add invividual stopwords to the standard ones
    en_stop = set(nltk.corpus.stopwords.words('english'))
    en_stop.update(stopwords)
    def prepare_text_for_lda(text):
        tokens = tokenize(text)
        tokens = [token for token in tokens if len(token) > 2]
        tokens = [token for token in tokens if token not in en_stop]
        tokens = [get_lemma(token) for token in tokens]
        return tokens
    text_data = []
    f = df.text
    for line in f:
        tokens = prepare_text_for_lda(line)
        text_data.append(tokens)
    from gensim import corpora
    #Build a gensim dictionary of the passed in text
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    import pickle
    pickle.dump(corpus, open('corpus.pkl', 'wb'))
    #Saves text structure
    dictionary.save('dictionary.gensim')
    import gensim

    ldamodel = gensim.models.ldamodel.LdaModel(corpus,
                    num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
    ldamodel.save('model5.gensim')
    #Prints the topic with the first four words
    topics = ldamodel.print_topics(num_words=4)
    for topic in topics:
        print(topic)
    #Loads the created infrastructure
    dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
    corpus = pickle.load(open('corpus.pkl', 'rb'))
    lda = gensim.models.ldamodel.LdaModel.load('model5.gensim')
    #Topic Modeling
    import pyLDAvis.gensim
    lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary,
                                                        sort_topics=False)
    return pyLDAvis.display(lda_display)
