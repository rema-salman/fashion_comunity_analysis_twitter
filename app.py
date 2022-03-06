import os

# Load EDA Pkgs
import pandas as pd
import numpy as np
 
import matplotlib.pyplot as plt
import seaborn as sns

# emotion detection lib
from nrclex import NRCLex

# Sentiment Analysis
from textblob import TextBlob

# Load ML Pkgs
# Estimators
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

# Transformers
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix


# helps with cleaning/extractions
import neattext.functions as nfx

df = pd.read_csv("data/merged_tweets.csv")

df.dropna() # drop rows if empty cell

print (df['is_retweet'])
# Create a list of reference and a function for flaging if any of ref was found in each tweet
ethical_ref = ['#ethical', 'ethical' 'ethicalfashion', '#ethicaljewelry', 'ethicaljewelry', '#ethicallymade', 
               'ethicallymade', 'ethicalpitch','#ethicalproduction', 'ethicalproduction', 'ethics', '#ethics',  
               '#fairtrade','fairtrade','fairtradelifestyle','fair','#fair', 'fairness', 'moral']

def identify_subject(tweet, refs):
    flag = 0 
    for ref in refs:
        if tweet.find(ref) != -1:
            flag = 1
    return flag
 
df['ethical_sorting'] = df['text'].apply(lambda x: identify_subject(x, ethical_ref)) 

# # Clean text
df['clean_tweet'] = df['text'].apply(lambda x: nfx.remove_userhandles(x))
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: nfx.remove_urls(x))
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: nfx.remove_emojis(x))
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: nfx.remove_currency_symbols(x))
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: nfx.remove_hashtags(x))
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: nfx.remove_dates(x))
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: nfx.remove_dates(x))
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: nfx.remove_numbers(x))
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: nfx.remove_puncts(x))
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: nfx.remove_stopwords(x))


# get polarity and subjectivity
def get_sentiment(text):
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    sentiment_subjectivity = blob.sentiment.subjectivity
    if sentiment_polarity > 0:
        sentiment_label = 'Positive'
    elif sentiment_polarity < 0:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'
    result = {'polarity':sentiment_polarity,
              'subjectivity':sentiment_subjectivity,
              'sentiment':sentiment_label}
    return result

df['sentiment_results'] = df['clean_tweet'].apply(lambda x: get_sentiment(x))
df = df.join(pd.json_normalize(df['sentiment_results']))

#visualize both sentiments
def visualize_value_count(value_counts, fig_name, x_lable, y_lable):
    plt.figure(figsize=(20, 10))
    value_counts.plot(kind='bar')
    plt.xticks(rotation=45,fontsize=25)
    plt.yticks(fontsize=25)
    plt.xlabel(x_lable,fontsize=25)
    plt.ylabel(y_lable,fontsize=25)
    plt.tight_layout()
    plt.savefig(f"img/{fig_name}.png")

# fillter the dataframe into eithcal and not tweets
ethical_sorted_df = df[df['ethical_sorting']==1] 
ethical_unsorted_df = df[df['ethical_sorting']==0] 
# getting value counts
ethical_sorted_value_counts = ethical_sorted_df['sentiment'].value_counts()
ethical_unsorted_value_counts = ethical_unsorted_df['sentiment'].value_counts()


# execute the function 
# visualize_value_count(ethical_sorted_value_counts, 'ethical_prespective_sentiment','Sentiment' , 'Count')
# visualize_value_count(ethical_unsorted_value_counts, 'rest_sentiment','Sentiment' , 'Count')
 
print(df.columns)
ax = df.plot(x="sentiment", y=ethical_sorted_value_counts, kind="bar")
df.plot(x="sentiment", y=ethical_unsorted_value_counts, kind="bar", ax=ax, color="C2")

# print (NRCLex(df['clean_tweet'].iloc[4]).top_emotions)
# print (  NRCLex(df['clean_tweet'].iloc[4]).affect_frequencies)