from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import config
import time
from influxdb import InfluxDBClient
import json
from pymongo import MongoClient

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_secret = config.access_secret

class StreamingListerner(StreamListener):

    def on_data(self, tweet_data):

        tweet_data_json = json.loads(tweet_data)

        client = MongoClient('localhost:27017')
        COVID = client.COVID
        Collection = COVID["Tweets"]
        Collection.insert_one(tweet_data_json)

        print(tweet_data_json)

        return True

    def on_error(self, status):
        print("Printing in on_error function :" + status)

if __name__ == '__main__':
    print("Twitter Streaming Application Started")

    covidStreamingListening = StreamingListerner()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token,access_secret)

    stream = Stream(auth, covidStreamingListening)

    stream.filter(track=['corona', 'covid','Coronavirus','Covid-19'])



