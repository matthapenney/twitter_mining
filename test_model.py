import tweepy

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

access_token = '798459160811581440-O0unJrt315izjrxHWABRYC7tNAsx3A8' 
access_token_secret = 'QNXzJ4b31WVLYH1KThrkDmNZyDMNwaVmqgXT5V7LaPWeq' 
consumer_key = 'dJZ1NjBIAL6XiDTRMuETwcDvP'
consumer_secret = '0GWZpu0Y2kih0Dgr7sL32S7FOIIOHYybQSCjXbxrbnEh6y0wOb'

auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
api = tweepy.API(auth)


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

# Loop over partner_list using funtion: partner_results
test_model = ['ultradavid', 'jchensor']

partner_results = dict()
for partner in test_model:
	param = []
	partner_results[partner] = partner_func(param,partner)

print(partner_results['ultradavid']['user_followers_count'].value_counts())
print(partner_results['jchensor']['user_followers_count'].value_counts())

print(partner_results['ultradavid']['retweet_count'])

