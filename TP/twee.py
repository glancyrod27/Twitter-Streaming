from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys  
import json
from datetime import datetime  
from elasticsearch import Elasticsearch
from geopy.geocoders import Nominatim
#from requests_aws4auth import AWS4Auth

#Variables that contains the user credentials to access Twitter API 
access_token = "919581457982640128-ullOyY52aA057rB3bBp0P0j7xBrEJFg"
access_token_secret = "7qnHxbaEE3NnG5XwAxC1IKGBZnPcuAWIWG6Gpl7LiOdpQ"
consumer_key = "ZSh6PfXZzVZl2iSrwpMXeiNkW"
consumer_secret = "sc7RXbO7LXocrdnuWfaube6VinvWx6HWKc0IxTvyEoLMnCf2xZ"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

es = Elasticsearch()

class listener(StreamListener):
  def on_data(self, data):
    tweet = json.loads(data)
    try:
      print tweet["coordinates"]["coordinates"]
    except:
      pass
    else:
      json_data = json.loads(data)
      id = str(json_data['id'])
      lat = json_data["coordinates"]["coordinates"][0]
      lon = json_data["coordinates"]["coordinates"][1]
      es.index(index="index1", id=id, doc_type="tweet", body={"tweets": tweets, "location" : {"lat":lat, "lon":lon}})
      print lat
      print lon
    return (True)

  def on_error(self, status):
    print status


def get_twitter_stream():
  try:
    twitterStream = Stream(auth, listener())
    twitterStream.filter(locations=[-180, -90, 180, 90])
  except:
    pass


if __name__ == "__main__":
  get_twitter_stream()