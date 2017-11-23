#!/usr/bin/env python
import tweepy
# from our keys module (keys.py), import the keys dictionary
# todo: implement this so you can reference a .py from another directory
from keys import keys
 
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
 

# K word up bitches. Here's the sitch. Pseudocode tiem.
#
# 1. Run an API call via Tweepy to search for tweets near saskatoon since 2013-11-23
# 2. Grab all "ungrabbed" search results and scribe it as a CSV file (maybe make a function to encode to CSV)
# 3. Sleep for 15 minutes, then do it again.
# 4. Do this for 24 hours and hopefully we'll go back three years.

# TODO: In the future, scrape tweets with the #yxe or #saskatoon hashtag as well.

twts = api.search(q="Hello World!")     
 
#list of specific strings we want to check for in Tweets
t = ['Hello world!',
    'Hello World!',
    'Hello World!!!',
    'Hello world!!!',
    'Hello, world!',
    'Hello, World!']
 
for s in twt:
    for i in t:
        if i == s.text:
            sn = s.user.screen_name
            m = "@%s Hello!" % (sn)
            s = api.update_status(m, s.id)