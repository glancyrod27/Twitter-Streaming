import sys  
import json
from datetime import datetime  
from elasticsearch import Elasticsearch

es = Elasticsearch()	
	
tweets_all= es.search(index="index1",size=1000, body={"query": {"match": {"tweets" : "love"}}})
print("Got %d Hits:" % tweets_all['hits']['total'])
tag="trump"
for hit in tweets_all['hits']['hits']:
    print(hit["_source"]["tweets"])
    print(hit["_source"]["location"]["lat"])
    print(hit["_source"]["location"]["lon"])
    print "\n"
# for line in tweets_all:
# 	try:
# 		tweet = json.loads(line.strip())
# 		print tweet
# 		print "/n*****/n"
# 	except Exception as e:
# 		raise e