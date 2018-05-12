import boto3
# import geocoder
# from geocoder import location
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream
import datetime
import json


c_key = "ZSh6PfXZzVZl2iSrwpMXeiNkW"
c_secret = "sc7RXbO7LXocrdnuWfaube6VinvWx6HWKc0IxTvyEoLMnCf2xZ"
a_token = "919581457982640128-ullOyY52aA057rB3bBp0P0j7xBrEJFg"
a_secret = "7qnHxbaEE3NnG5XwAxC1IKGBZnPcuAWIWG6Gpl7LiOdpQ"

sqs = boto3.resource('sqs')

#queue = sqs.create_queue(QueueName ='', Attributes={'DelaySeconds':'5'})
q = sqs.get_queue_by_name(QueueName='')
print (q.url)
print(q.attributes.get('DelaySeconds'))



class listener(StreamListener):
    def on_data(self, raw_data):
        print(raw_data)
        all_data = json.loads(raw_data)
        loc_en = all_data["user"]["geo_enabled"]
        lang = all_data["user"]["lang"]
        create_time = all_data["created_at"]
        current_time = datetime.datetime.now()
        print create_time
        print current_time

        if 'text' in all_data and loc_en and lang == "en":
            tweets = all_data["retweeted_status"]["text"]

            username = all_data["user"]["screen_name"]
            location = all_data["user"]["location"]

            response = q.send_message(MessageBody=tweets,
                                      MessageAttributes={
                                          'language': {
                                              'DataType': 'String',
                                              'StringValue': lang
                                          },
                                          'location': {
                                              'DataType': 'Number',
                                              'StringValue': location
                                          },
                                      })



    def on_error(self, status_code):
        print (status_code)

    

auth = OAuthHandler(c_key, c_secret)
auth.set_access_token(a_token, a_secret)

twitterStream = Stream(auth, listener())
terms = [
        'kohli', 'modi'
        ,'hollywood','bollywood', 'trump', 'them', 'this', 'india'
        ]

while True:
    try:
        twitterStream.filter(track=terms)
    except:
        continue