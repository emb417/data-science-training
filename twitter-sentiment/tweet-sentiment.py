import sys
import json

afinnfile = open(sys.argv[1])
scores = {} # initialize an empty dictionary
for line in afinnfile:
  term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
  scores[term] = int(score)  # Convert the score to an integer.

#print scores.items() # Print every (term, score) pair in the dictionary

outputfile = open(sys.argv[2])
tweets = [] # initializes tweets list
for line in outputfile:
	tweets.append(json.loads(line)) # builds list by formatting lines from output file

for tweet in tweets:
	tweet_score = 0 #track score in a tweet
	if tweet.has_key("text") and tweet["text"] != None and tweet["text"] != "":	
		words = tweet["text"].split() #split tweet into individual words
		for word in words:
			if scores.has_key(word.encode('ascii','ignore')): #check if scores has the key, also coverting unicode to ascii for better matching
				tweet_score += scores[word.encode('ascii','ignore')] #add up score
		print tweet_score #print tweet score