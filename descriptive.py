import os
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# helps with cleaning/extractions
import neattext.functions as nfx



df = pd.read_csv("data/merged_tweets.csv", index_col=[0])

print (df.shape)
print (df.columns)
"""
function executes most frequent sources and plots them and saves the plot into a file.  
"""
def visualize_value_count(df, fig_name, x_lable, y_lable):
    # df.unique()
    plt.figure(figsize=(20, 10))
    df.value_counts().nlargest(10).plot(kind='bar')
    plt.xticks(rotation=45,fontsize=25)
    plt.yticks(fontsize=25)
    plt.xlabel(x_lable,fontsize=25)
    plt.ylabel(y_lable,fontsize=25)
    plt.tight_layout()
    plt.savefig(f"img/{fig_name}.png")



visualize_value_count(df['user_name'], "user_name", "Top active users","# of tweets")
visualize_value_count(df['user_location'], "user_location", "Top locations of tweeting","# of tweets")
visualize_value_count(df['source'], "source", "Top sources used for tweeting","# of tweets")
# visualize_value_count(df['user_followers'], "user_followers")
# visualize_value_count(df['user_friends'], "user_friends")
# visualize_value_count(df['user_favourites'], "user_favourites")


