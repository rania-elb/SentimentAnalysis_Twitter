# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import pymongo
from pymongo import MongoClient
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime
from nltk.tokenize import word_tokenize
import re
import operator 
from collections import Counter
from nltk.corpus import stopwords
import string


# The MongoDB connection info. This assumes your database name is TwitterStream, and your collection name is tweets.
client = MongoClient('localhost')
db = client.TwitterData_Macron
db.tweet_data.create_index([("id", pymongo.ASCENDING)],unique = True) # make sure the collected tweets are unique
collection = db.tweet_data_macron

# Add the keywords you want to track. They can be cashtags, hashtags, or words.
keywords = ['#Macron']

# Optional - Only grab tweets of specific language
language = ['en']

# You need to replace these with your own values that you get after creating an app on Twitter's developer portal.
consumer_key = "iHiVsusTqlexDmCB2C5krA3h1"
consumer_secret = "UEPVSObOzjeB3e3QeDa3zGlNVUi31nw5G3IFS17K2m3L1jsJi4"
access_token = "852253511085641730-AHuG9HU4q1zyyv4utU8YDvFKBA21IB7"
access_token_secret = "pRGiGzQy264t18SBvyWIJmiDOH7CC11Hj8QRj36a7qfbp"

# The below code will get Tweets from the stream and store only the important fields to your database
class StdOutListener(StreamListener):

    def on_data(self, data):

        # Load the Tweet into the variable "t"
        t = json.loads(data)

        # Pull important data from the tweet to store in the database.
        tweet_id = t['id_str']  # The Tweet ID from Twitter in string format
        username = t['user']['screen_name']  # The username of the Tweet author
        followers = t['user']['followers_count']  # The number of followers the Tweet author has
        text = t['text']  # The entire body of the Tweet
        hashtags = t['entities']['hashtags']  # Any hashtags used in the Tweet
        dt = t['created_at']  # The timestamp of when the Tweet was created
        language = t['lang']  # The language of the Tweet

        # Convert the timestamp string given by Twitter to a date object called "created". This is more easily manipulated in MongoDB.
        created = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')

        # Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
        tweet = {'id':tweet_id, 'username':username, 'followers':followers, 'text':text, 'hashtags':hashtags, 'language':language, 'created':created}

        # Save the refined Tweet data to MongoDB
        collection.save(tweet)

        

    # Prints the reason for an error to your console
    def on_error(self, status):
        print status

# Some Tweepy code that can be left alone. It pulls from variables at the top of the script
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=keywords, languages=language)




