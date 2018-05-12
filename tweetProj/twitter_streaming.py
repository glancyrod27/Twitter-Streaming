#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys  
import json
from datetime import datetime  
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

#Variables that contains the user credentials to access Twitter API 

awsauth = AWS4Auth(aws_access_key_id,aws_secret_access_key,'us-east-2', 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        json_data = json.loads(data)
        if 'text' in json_data:
            tweets = json_data['text'].lower().encode('ascii','ignore').decode('ascii')
            location = json_data['user']['location']
            id = str(json_data['id'])
            lon = None
            lat = None
            if json_data['coordinates']:
                lat = float(json_data['coordinates']['coordinates'][0])
                lon = float(json_data['coordinates']['coordinates'][1])
            elif 'place' in json_data.keys() and json_data['place']:
                lat = float(json_data['place']['bounding_box']['coordinates'][0][0][0])
                lon = float(json_data['place']['bounding_box']['coordinates'][0][0][1])
            if lat and lon:
                try:
                    es.index(index="index1", doc_type="tweet", body={"tweets": tweets, "location" : {"lat":lat, "lon":lon}})
                except Exception:
                    pass

    def on_error(self, status):
        print status        

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
   
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    es.index(index="index1", doc_type="tweet", body={"tweets": "tweets", "location" : {"lat":"34.00", "lon":"67.90"}})
    es.indices.delete(index='index1', ignore=[400, 404])

    try:
        l = StdOutListener()
        stream = Stream(auth, l)
        stream.filter(locations=[-180,-90,180,90])
    except Exception as e:
        raise e
    