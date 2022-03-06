import os
import pandas as pd
 
import matplotlib.pyplot as plt



df = pd.read_csv("data/merged_tweets.csv")

df['date'] = pd.to_datetime(df['date'],errors='coerce') #format='%Y-%m-%d %H:%M:%S'

# df['day'] = df['date'].apply(lambda x: x.weekday())
df['day'] = df['date'].apply(lambda x: x.date())

days = df.groupby('day')
day_count = days['text'].count()
timedict = day_count.to_dict()


print(timedict)
#  Plot time-serise
weekday_dict = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
plt.figure(figsize=(20, 10))
# plt.plot(list(weekday_dict.values()), list(timedict.values()), color='blue') 
plt.plot(list(timedict.keys()), list(timedict.values()), color='blue') 

plt.xlabel('Date',fontsize=25)
plt.ylabel("# of tweets",fontsize=25)
plt.xticks(list(timedict.keys()),rotation=45,fontsize=25)
plt.yticks(fontsize=25)
plt.tight_layout()
plt.savefig(f"img/daily_distribution1.png")


