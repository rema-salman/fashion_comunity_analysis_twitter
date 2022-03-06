import os
import tweepy 
import pandas as pd
from tqdm import tqdm 


auth = tweepy.OAuthHandler('wFgKQYw3pzpp5uSdjUWIPSsiK', 'NKZUrKppwzNMWdtnfdgr6vdrtao7eSCBEML6rm58JSgii053lS')
auth.set_access_token('1313549581284712449-qIpeoUN7sZrO6zOkNZNOz39RZg44aJ', 'zRFIYd77Lrs3HILTpXNXNajdXvnsqN70WleMSmk5UhlVz')

api = tweepy.API(auth,wait_on_rate_limit=True)

search_words = ["#fashion", "#sustainablefashion", "#SustainableFashion", '#slowfashion', '#ethicalfashion','#ethicallymade', 'ethicallymade', '#fairtrade', '#ecofashion']

for x in search_words:
    # Collect tweets
    tweets = tweepy.Cursor(api.search_tweets,
                q=x,
                since_date = "2021-10-01",
                lang="en").items(500)

    #Populate the dataset(object-> list)
    tweets_copy = []
    for tweet in tqdm(tweets):
        tweets_copy.append(tweet)
    print(f"new tweets retrieved: {len(tweets_copy)}")

        # Populate the dataset(framework)
    tweets_df = pd.DataFrame()
    for tweet in tqdm(tweets_copy):
        hashtags = []
        try:
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
            text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
        except:
            pass
        tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name, 
                                                    'user_id': tweet.user.id,
                                                    'user_location': tweet.user.location,
                                                    'user_description': tweet.user.description,
                                                    'user_created': tweet.user.created_at,
                                                    'user_followers': tweet.user.followers_count,
                                                    'user_friends': tweet.user.friends_count,
                                                    'user_favourites': tweet.user.favourites_count,
                                                    'user_verified': tweet.user.verified,
                                                    'date': tweet.created_at,
                                                    'text': text,
                                                    'in_reply_to_screen_name': tweet.in_reply_to_screen_name, 
                                                    'hashtags': [hashtags if hashtags else None],
                                                    'source': tweet.source,
                                                    'is_retweet': tweet.retweeted}, index=[0]))


        # tweets_df.head()
        #5. Save the data
        #5.1. Read past data
    tweets_old_df = pd.read_csv("data/fashion_tweets.csv")
    print(f"past tweets: {tweets_old_df.shape}")

        #5.2. Merge past and present data
    tweets_all_df = pd.concat([tweets_old_df, tweets_df], axis=0)
    print(f"new tweets: {tweets_df.shape[0]} past tweets: {tweets_old_df.shape[0]} all tweets: {tweets_all_df.shape[0]}")

        #5.3. Drop duplicates
    tweets_all_df.drop_duplicates(subset = ["user_name", "date", "text"], inplace=True)
    print(f"all tweets: {tweets_all_df.shape}")

    #5.4. Export the updated data
    tweets_all_df.to_csv("data/fashion_tweets.csv", index=False)