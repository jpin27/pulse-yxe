#!/usr/bin/env python
import tweepy
import time
import sys
import jsonpickle

# from tweepy import Stream
# from tweepy.streaming import StreamListener

# from our keys module (keys.py), import the keys dictionary
from keys import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

IS_DATAMINED = True

# Some authentication stuff. Magic. Don't touch.
# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Stop mining when rate limit is exceeded and wait for 15 minutes
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
 
#Error handling
if (not api):
	print ("Problem Connecting to API")

# Saskatoon id is:  4bb41f9d86e16416
 
# Let's define an error handler.
def getExceptionMessage(msg):
	words = msg.split(' ')

	errorMsg = ""
	for index, word in enumerate(words):
		if index not in [0,1,2]:
			errorMsg = errorMsg + ' ' + word
	errorMsg = errorMsg.rstrip("\'}]")
	errorMsg = errorMsg.lstrip(" \'")

	return errorMsg

# Little thing to make sure the auth credentials work.
def doSanityCheck():
	try:
		user = api.me()
	except tweepy.TweepError as e:
		print (e.api_code)
		print (getExceptionMessage(e.reason))

	print('Mining under the name ' + user.name
		+ ' from ' + user.location
		+ ' following ' + str(user.friends_count) 
		+ ' people.')

#export PYTHONIOENCODING=utf-8
#export ConEmuDefaultCp=65001


############ BEGIN DATAMINER ############

#This is what we are searching for
#We can restrict the location of tweets using place:id 
#We can search for multiple phrases using OR
searchQuery = 'place:4bb41f9d86e16416 OR #saskatoon OR #yxe OR saskatoon OR yxe'

#Search 1 million tweets
maxTweets = 1000000

#The twitter Search API allows up to 100 tweets per query
tweetsPerQry = 100
tweetCount = 0

#Open a text file to save the tweets to
with open('stoonTweets.json', 'a') as f:

	#Tell the Cursor method that we want to use the Search API (api.search)
	#Also tell Cursor our query, and the maximum number of tweets to return
	for tweet in tweepy.Cursor(api.search,q=searchQuery).items(maxTweets) :         

		#Verify the tweet has place info before writing (It should, if it got past our place filter)
		if tweet.place is not None:
			
			#Write the JSON format to the text file, and add one to the number of tweets we've collected
			f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
			tweetCount += 1

		#Display how many tweets we have collected
		print("Downloaded {0} tweets".format(tweetCount))

############ END DATAMINER ############
