# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import json
from datetime import datetime
from elasticsearch import Elasticsearch

# Variables that contains the user credentials to access Twitter API
access_token = "912800103475359744-2EV9H3FW2Tb9Fyj3ZfiZ6GSVoLj3gMp"
access_token_secret = "EpHrPOF2Ycx1avEOlFxNTIZh07WbOwuZiJwm6cVRCnOBZ"
consumer_key = "2BsJ9XVxFgNsG2HsAbQCpwgNG"
consumer_secret = "KliwIqpgrYnEmDcz0ZiTfsMRR3BYo7Eg7bamfR8GGl8IVpQDP2"




# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        if len(host) == 0:
            es = Elasticsearch()
        else:
            es = Elasticsearch(host)
        try:
            json_data = json.loads(data)
            tweet = json_data['text']
            id = str(json_data['id'])
            lon = None
            lat = None
            if json_data['coordinates']:
                lon = float(json_data['coordinates']['coordinates'][0])
                lat = float(json_data['coordinates']['coordinates'][1])
            elif 'place' in json_data.keys() and json_data['place']:
                lon = float(json_data['place']['bounding_box']['coordinates'][0][0][0])
                lat = float(json_data['place']['bounding_box']['coordinates'][0][0][1])
            elif 'retweeted_status' in json_data.keys() and 'place' in json_data['retweeted_status'].keys() and \
                    json_data['retweeted_status']['place']:
                lon = float(json_data['retweeted_status']['place']['bounding_box']['coordinates'][0][0][0])
                lat = float(json_data['retweeted_status']['place']['bounding_box']['coordinates'][0][0][1])
            elif 'quoted_status' in json_data.keys() and 'place' in json_data['quoted_status'].keys() and \
                    json_data['quoted_status']['place']:
                lon = float(json_data['quoted_status']['place']['bounding_box']['coordinates'][0][0][0])
                lat = float(json_data['quoted_status']['place']['bounding_box']['coordinates'][0][0][1])
            if lat and lon:
                es.index(index=index_name, id=id, doc_type="tweet",
                         body={"tweet": tweet, "location": {"lat": lat, "lon": lon}})
        except Exception as e:
            print("ERROR: " + str(e))

    # def on_data(self, data):
    #     print(data)

    def on_error(self, status):
        print(status)

if len(sys.argv)<3:
    print ("Usage\n\npython live_elastic_search.py <index_name> <host of elastic search>\n")
if __name__ == '__main__':
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(languages=['en'], track=['starbucks','android','national geographic','pets','music'])