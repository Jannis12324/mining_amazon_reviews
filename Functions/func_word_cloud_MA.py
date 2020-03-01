import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
print(("Function <make_wordcloud> now available. Include the following"+
        " arguments: \n")+
        ("df: A dataframe with the column <reviews> that have been cleaned \n")+
        ("exclude_words: A list of words that should not be included in the"+
        " wordcloud \n")+
        ("filename: The filename that ends with .png, as a string. It will"+
        " be saved in Figures->wordclouds"))
def make_wordcloud(df, exclude_words, filename):
    #Make sure the df already has a cleaned "reviews" column
    text = " ".join(review for review in df.reviews)
    stopwords = set(STOPWORDS)
    stopwords.update(exclude_words)
    # Generate a word cloud image
    wordcloud = WordCloud(stopwords=stopwords,colormap= "winter", width= 400,
                        height = 400, background_color="white").generate(text)
    # Display and save the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    figpath = 'C:\\Users\\...\\wordclouds\\'
    wordcloud.to_file(figpath+filename)
    return plt.show()
