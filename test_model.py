import tweepy

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import vincent

sns.set_context("notebook")
sns.set_palette('Set2', 10)

access_token = '' 
access_token_secret = '' 
consumer_key = ''
consumer_secret = ''

auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
api = tweepy.API(auth)


def partner_func(param,partner):

	for tweet in tweepy.Cursor(api.user_timeline, screen_name = partner).items():
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

# Loop over partner_list using funtion: partner_results
test_model = ['ultradavid', 'jchensor', 'glookoinc']

partner_results = dict()
for partner in test_model:
	param = []
	partner_results[partner] = partner_func(param,partner)
	partner_results[partner].to_csv('partner_results[%s].csv' %(partner), sep ='\t')

print(partner_results['ultradavid']['user_followers_count'].value_counts())
print(partner_results['jchensor']['user_followers_count'].value_counts())

def influence(df):
    internal = np.sqrt(df.user_followers_count.apply(lambda x: x + 1))
    external = np.sqrt(df.retweet_count.apply(lambda x: x + 1))
    df['influence'] = internal * external
    return df


for partner in test_model:
	influence(partner_results[partner])

	print(partner_results[partner].influence.mean())

# print(partner_results['ultradavid'].iloc[[28]])


# Filter out retweets

no_RT = ~partner_results['ultradavid']['text'].str.contains('RT')


num_favs = dict()
num_retweets = dict()
for person in test_model:
	num_favs[person] = partner_results[person]['favorite_count'].sum()
	num_retweets[person] = partner_results[person]['retweet_count'].sum()
	print("Number of favorited tweets for %s :" % (person), num_favs[person])
	print("Number of retweeted tweets for %s :" % (person), num_retweets[person])


fav_stats = (num_favs['jchensor'],num_favs['glookoinc'])
re_stats = (num_retweets['jchensor'], num_retweets['glookoinc'])




ul_fol = partner_results['ultradavid']['user_followers_count'].mean()
j_fol = (partner_results['jchensor']['user_followers_count'].mean())




plt.show()


