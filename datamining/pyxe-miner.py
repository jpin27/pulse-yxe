#!/usr/bin/env python
import tweepy
import time
import sys
import json
import jsonpickle
import pandas as pd

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

# This method creates a pandas dataframe with the JSON input file
def pop_tweets(inputFile):

    # Project proposal outlines these columns: 
    # text, author, timestamp, hashtags, retweet count, location (for geotagged tweets), and source

    #Declare a new data frame with pandas, with some specific column names
    tweets = pd.DataFrame(columns=[
    	'userHandle','text','timestamp','location','retweet count','source'
    	])

    #Open the text file that contains the tweets we collected
    tweets_file = open(inputFile, "r")
    
    #Read the text file line by line
    for line in tweets_file:
        
        #Load the JSON information
        tweet = json.loads(line)
        
        #If the tweet isn't empty, add it to the data frame
        if ('text' in tweet): 
            tweets.loc[len(tweets)]=[tweet['user']['screen_name'],tweet['text'],\
            	tweet['created_at'],tweet['place']['full_name'],tweet['retweet_count'],\
            	tweet['source']
            ]    

    return tweets

#export PYTHONIOENCODING=utf-8
#export ConEmuDefaultCp=65001


############ BEGIN DATAMINER ############

if IS_DATAMINED is not True:

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

else:
	print("DATAMINING IS DONE MOTHAFUCKAAAAAA")

############ END DATAMINER ############




############ BEGIN ANALYSIS ############


yxe_tweets = pop_tweets('stoonTweets.json')

yxe_tweets.head(n=5)
print(yxe_tweets['text'][4])


# with open('stoonTweets.json', 'r') as f:
# 	line = f.readline() # read only the first tweet/line
# 	tweet = json.loads(line) # load it as Python dict
# 	print(json.dumps(tweet, indent=4)) # pretty-print

############ END ANALYSIS ############


############ CSV SERIES ############

# # Open/create a file to append data to
# csvFile = open('result.csv', 'a')

# #Use csv writer
# csvWriter = csv.writer(csvFile)

# for tweet in tweepy.Cursor(api.search,
# 	q = "saskatoon",
# 	since = "2017-11-27",
# 	# until = "2014-02-15",
# 	lang = "en",
# 	tweet_mode = "extended").items(100):

# 	if 'retweeted_status' in dir(tweet):
# 		fullTextTweet = tweet.retweeted_status.full_text
# 	else:
# 		fullTextTweet = tweet.full_text
	
#     # Write a row to the CSV file. I use encode UTF-8
# 	csvWriter.writerow([tweet.created_at, fullTextTweet.encode('utf-8')])
# 	print(tweet.created_at, fullTextTweet)
# csvFile.close()

############ END CSV SERIES ############