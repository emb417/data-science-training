import sys
import json
from collections import OrderedDict

tweetfile = open(sys.argv[1])
tweets = [] # initializes tweets list
for line in tweetfile:
	tweets.append(json.loads(line)) # builds list by formatting lines from output file

"""
"entities":{"hashtags":[{"text":"Shoes","indices":[23,29]}]
print <hashtag:string> <frequency:float>
"""

hashtags = {}
for tweet in tweets:
	if tweet.has_key("entities") \
	and tweet["entities"] != None \
	and tweet["entities"].has_key("hashtags") \
	and tweet["entities"]["hashtags"] != None:
		for hashtag in tweet["entities"]["hashtags"]:
			if hashtag.has_key("text") and hashtag["text"] != None:
				if hashtags.has_key(hashtag["text"]):
					hashtags[hashtag["text"]] = hashtags[hashtag["text"]]+1 #increase count
				elif hashtag["text"] != "":
					hashtags[hashtag["text"]] = 1 #initialize dictionary of hashtags
	
sorted_hashtags = sorted(hashtags.items(), key=lambda t: t[1])
sorted_hashtags.reverse()
"""
print top ten hashtags
"""
i = 0
for hashtag in sorted_hashtags:
	if i < 10:
		print hashtag[0] + " " + str(hashtag[1])
		i += 1
