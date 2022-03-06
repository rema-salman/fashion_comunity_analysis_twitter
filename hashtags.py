import os
import tweepy 
import pandas as pd
import numpy as np
 
import matplotlib.pyplot as plt
import seaborn as sns

# emotion detection lib
from nrclex import NRCLex
import neattext.functions as nfx
from tweepy.models import Relationship






df = pd.read_csv("data/merged_tweets.csv")

df.dropna() # drop rows if empty cell
 


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

# fillter the dataframe into eithcal and not tweets
ethical_sorted_df = df[df['ethical_sorting']==1] 
 

df['user_handlers'] = df['text'].apply(lambda x: nfx.extract_userhandles(x))
# print (df['user_handlers'])

Name_List = list(df["user_name"])
mentions_List = list(df["user_handlers"])



print(mentions_List) 
