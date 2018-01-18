import pymongo
from pymongo import MongoClient


#connect to Database
connection = MongoClient('localhost', 27017)
db = connection.tweet_db


#handle to friends Collection
data = db.tweet_collection


tweets = data.find()

with open("C:\\Users\\hp\\Documents\\Projects5\\code\\twitter-sentiment-analysis-master\\retrived_tweets.csv",'wb') as file:
    
    for item in tweets:
        file.writelines(item["text"].encode(encoding = 'UTF-8'))
        #print("Tweet: " + item["text"].encode(encoding = 'UTF-8'))
        file.write("\n")
