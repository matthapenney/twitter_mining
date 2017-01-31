import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
sns.set_context("notebook")
sns.set_palette('Set2', 10)

#User Credentials

access_token = '' 
access_token_secret = '' 
consumer_key = ''
consumer_secret = ''

auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
api = tweepy.API(auth)

# Query all tweets with "diabetes" in past week or so

search_words = ['diabetes']

results = api.search(q = search_words)
print(len(results))

def print_tweet(tweet):
	print("@%s - %s (%s)" % (tweet.user.screen_name, tweet.user.name, tweet.created_at))
	print(tweet.text)

tweet = results[0]
print_tweet(tweet)

tweet = results[1]

for x in dir(tweet):
	if not x.startswith("_"):
		print("%s : %s" % (x, eval('tweet.' + x)))

# Inspect User Object

user = tweet.author

for x in dir(user):
	if not x.startswith("_"):
		print("%s : %s" % (x, eval("user." + x)))

# results stands for search results (based upon word search)
results = []

for tweet in tweepy.Cursor(api.search, q = search_words).items(100):
	results.append(tweet)
print(len(results))

#Store in DataFrame

def get_results(results):
	id_list = [tweet.id for tweet in results]
	data_set = pd.DataFrame(id_list, columns = ['id'])

	#Process Tweet Data

	data_set['text'] = [tweet.text for tweet in results]
	data_set['created_at'] = [tweet.created_at for tweet in results]
	data_set['retweet_count'] = [tweet.retweet_count for tweet in results]
	data_set['favorite_count'] = [tweet.favorite_count for tweet in results]
	data_set['source'] = [tweet.source for tweet in results]

	# Process User Data
	data_set['user_id'] = [tweet.author.id for tweet in results]
	data_set['user_screen_name'] = [tweet.author.screen_name for tweet in results]
	data_set['user_name'] = [tweet.author.name for tweet in results]
	data_set['user_followers_count'] = [tweet.author.followers_count for tweet in results]
	data_set['user_friends_count'] = [tweet.author.friends_count for tweet in results]
	data_set['user_location'] = [tweet.author.location for tweet in results]

	return data_set

data_set = get_results(results)

# Timeline query based on user
t_results = api.user_timeline(screen_name = 'glookoinc')


# t_results stands for timeline_results (based upon @user search)
t_results =[]

for tweet in tweepy.Cursor(api.user_timeline, screen_name = 'glookoinc').items(100):
	t_results.append(tweet)
len(t_results)

def timeline_results(t_results):
	id_list = [tweet.id for tweet in t_results]
	timeline_set = pd.DataFrame(id_list, columns = ['id'])

	#Process Tweet Data

	timeline_set['text'] = [tweet.text for tweet in t_results]
	timeline_set['created_at'] = [tweet.created_at for tweet in t_results]
	timeline_set['retweet_count'] = [tweet.retweet_count for tweet in t_results]
	timeline_set['favorite_count'] = [tweet.favorite_count for tweet in t_results]
	timeline_set['source'] = [tweet.source for tweet in t_results]

	# Process User Data
	timeline_set['user_id'] = [tweet.author.id for tweet in t_results]
	timeline_set['user_screen_name'] = [tweet.author.screen_name for tweet in t_results]
	timeline_set['user_name'] = [tweet.author.name for tweet in t_results]
	timeline_set['user_followers_count'] = [tweet.author.followers_count for tweet in t_results]
	timeline_set['user_friends_count'] = [tweet.author.friends_count for tweet in t_results]
	timeline_set['user_location'] = [tweet.author.location for tweet in t_results]

	return timeline_set
timeline_set = timeline_results(t_results)

who = timeline_set['user_screen_name'].value_counts()


def partner_func(param,partner):

	for tweet in tweepy.Cursor(api.user_timeline, screen_name = partner).items(100):
		param.append(tweet)

	#Save each partner to pandas dataframe
	id_list = [tweet.id for tweet in param]
	partner_results[partner] = pd.DataFrame(id_list, columns = ['id'])

	#Process Tweet Data

	partner_results[partner]['text'] = [tweet.text for tweet in param]
	partner_results[partner]['created_at'] = [tweet.created_at for tweet in param]
	partner_results[partner]['retweet_count'] = [tweet.retweet_count for tweet in param]
	partner_results[partner]['favorite_count'] = [tweet.favorite_count for tweet in param]
	partner_results[partner]['source'] = [tweet.source for tweet in param]

	# Process User Data
	partner_results[partner]['user_id'] = [tweet.author.id for tweet in param]
	partner_results[partner]['user_screen_name'] = [tweet.author.screen_name for tweet in param]
	partner_results[partner]['user_name'] = [tweet.author.name for tweet in param]
	partner_results[partner]['user_followers_count'] = [tweet.author.followers_count for tweet in param]
	partner_results[partner]['user_friends_count'] = [tweet.author.friends_count for tweet in param]
	partner_results[partner]['user_location'] = [tweet.author.location for tweet in param]

	return partner_results[partner]

def influence(df):
    internal = np.sqrt(df.user_followers_count.apply(lambda x: x + 1))
    external = np.sqrt(df.retweet_count.apply(lambda x: x + 1))
    df['influence'] = internal * external
    return df

# Loop over partner_list using funtion: partner_results
# PARTNER LIST

partner_list = ['glookoinc','medtronic', 'myomnipod', 'TandemDiabetes', 'onetouch', 'accuchek_us', 'freestylediabet']

partner_results = dict()
for partner in partner_list:
	param = []
	partner_results[partner] = partner_func(param,partner)

	# Save each company info dataframe to csv file
	partner_results[partner].to_csv('partner_results[%s].csv' %(partner), sep ='\t')

std_list = []
for partner in partner_list:
	influence(partner_results[partner])

	print(" %s influence :" % (partner), partner_results[partner].influence.mean())
	std_list.append(partner_results[partner].influence.std())


#Analysis

# of favorited tweets in dataset
# of retweets total (according to timeline query)

num_favs = dict()
num_retweets =dict()
for company in partner_list:
	num_favs[company] = partner_results[company]['favorite_count'].sum()
	num_retweets[company] = partner_results[company]['retweet_count'].sum()
	print("Number of favorited tweets for %s :" % (company), num_favs[company])
	print("Number of retweeted tweets for %s :" % (company), num_retweets[company])

plt.figure()
df2 = pd.DataFrame({'User': ['glookoinc','medtronic', 'myomnipod', 'TandemDiabetes', 'onetouch', 'accuchek_us', 'freestylediabet'],'Influence': [79.50074959263794, 508.3761903083065, 43.35717865391955, 79.65391592356734, 110.34720685630455, 167.91010883106276, 156.04381585407523]})
#df3.plot("User", "Influence", kind = 'barh', color = color)
sns.barplot(x= 'User', y = 'Influence', data =df2)
plt.title('Twitter Account Influence')

monitor_list = ['medtronic', 'myomnipod', 'TandemDiabetes']
meter_list = ['onetouch', 'accuchek_us', 'freestylediabet']

follower_count = []
for partner in monitor_list:
	follower_count.append(partner_results[partner].user_followers_count.mean())
print(follower_count)

mfollower_count =[]
for partner in meter_list:
	mfollower_count.append(partner_results[partner].user_followers_count.mean())
print(mfollower_count)

plt.figure()
df3 = pd.DataFrame({'Partner': monitor_list, 'Followers': follower_count})
sns.barplot(x = 'Partner', y = 'Followers', data = df3)
plt.title('Twitter Account Followers')

plt.figure()
df4 = pd.DataFrame({'Partner': meter_list, 'Followers': mfollower_count})
sns.barplot(x = 'Partner', y = 'Followers', data = df4)
plt.title('Twitter Account Followers')

plt.show()
