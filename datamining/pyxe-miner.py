#!/usr/bin/env python
import tweepy
import time
import sys
import csv

# from our keys module (keys.py), import the keys dictionary
from keys import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

# Some authentication stuff. Magic. Don't touch.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
 
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

# K word up bitches. Here's the sitch. Pseudocode tiem.
#
# 1. Run an API call via Tweepy to search for tweets near saskatoon since 2013-11-23
# 2. Grab all "ungrabbed" search results and scribe it as a CSV file (maybe make a function to encode to CSV)
# 3. Sleep for 15 minutes, then do it again.
# 4. Do this for 24 hours and hopefully we'll go back three years.

# TODO: In the future, scrape tweets with the #yxe or #saskatoon hashtag as well.


doSanityCheck()

for tweet in tweepy.Cursor(
	api.search,
	q = "saskatoon",
	count = 100,
	).items(100):
    
    	print(tweet.created_at, tweet.text.encode('UTF8'))
    	print('\n')

# for tweet in tweepy.Cursor(api.search,
# 	q = "google",
# 	since = "2014-02-14",
# 	until = "2014-02-15",
# 	lang = "en").items():
# 		print(tweet.created_at, tweet.text)







# Boilerplate code. Use as basis. Delete if necessary.
# twts = api.search(q="Hello World!") 
# #list of specific strings we want to check for in Tweets
# t = ['Hello world!',
#     'Hello World!',
#     'Hello World!!!',
#     'Hello world!!!',
#     'Hello, world!',
#     'Hello, World!']

# s = 
# for s in twt:
#     for i in t:
#         if i == s.text:
#             sn = s.user.screen_name
#             m = "@%s Hello!" % (sn)
#             s = api.update_status(m, s.id)

# for s in twt:
#     for i in t:
#         if i == s.text:
#             sn = s.user.screen_name
#             m = "@%s Hello!" % (sn)
#             s = api.update_status(m, s.id)

