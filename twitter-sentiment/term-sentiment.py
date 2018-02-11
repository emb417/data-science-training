import sys
import json

afinnfile = open(sys.argv[1])
scores = {} # initialize an empty dictionary
for line in afinnfile:
  term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
  scores[term] = int(score)  # Convert the score to an integer.

outputfile = open(sys.argv[2])
tweets = [] # initializes tweets list
for line in outputfile:
	tweets.append(json.loads(line)) # builds list by formatting lines from output file

tweets_with_sent = []
correlated_sent_words = {}
for tweet in tweets:
	tweet_score = 0 #track score in a tweet
	if tweet.has_key("text") and tweet["text"] != None and tweet["text"] != "":
		words = tweet["text"].split() #split tweet into individual words
		for word in words:
			ascii_word = word.encode('ascii','ignore') #coverting unicode to ascii for better matching and ignoring non english chars
			if scores.has_key(ascii_word): #check if scores has the matching key
				tweet_score += scores[ascii_word] #add up score
		if tweet_score <> 0:
			tweets_with_sent.append({"score":tweet_score,"words":words})

"""
gather words in tweets with sent that are not in afinnfile
iterate through words in tweet and grab corresponding tweet score
calculate average score as correlated sent word score
should run tests against scores to determine if average is a good predictor
"""

for tweet in tweets_with_sent:
	for word in tweet['words']:
		ascii_word = word.encode('ascii','ignore') #encoding to ascii for better matching
		ascii_word = ascii_word.lower() #lower case all words for better aggregation, assuming case doesn't change sentiment correlation
		if scores.has_key(ascii_word):
			pass #skip over words in afinnfile
		else:
			if correlated_sent_words.has_key(ascii_word):
				count = correlated_sent_words[ascii_word]['count']+1 #increment count to calc rolling average
				score = (((count-1)*correlated_sent_words[ascii_word]['score'])+float(tweet['score']))/count #calc rolling average to use as weighted sent
				correlated_sent_words[ascii_word] = {'count':count,'score':score} #save count and score for next occurrence or printing
			else:
				correlated_sent_words[ascii_word] = {'count':1,'score':float(tweet['score'])} #initialize dictionary of correlated sent words

for word in sorted(correlated_sent_words):
	print word + " " + str(correlated_sent_words[word]['score'])
