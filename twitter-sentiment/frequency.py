import sys
import json

tweetfile = open(sys.argv[1])
tweets = [] # initializes tweets list
for line in tweetfile:
	tweets.append(json.loads(line)) # builds list by formatting lines from output file

"""
frequency = [# of occurrences of the term in all tweets]/[# of occurrences of all terms in all tweets]
print <term:string> <frequency:float>
"""

tweeted_words = {}
word_count = float(1) #track all words in all tweets
for tweet in tweets:
	if tweet.has_key("text") and tweet["text"] != None and tweet["text"] != "":
		words = tweet["text"].split() #split tweet into individual words
		for word in words:
			ascii_word = word.encode('ascii','ignore') #coverting unicode to ascii for better matching and ignoring non english chars
			ascii_word = ascii_word.lower() #lower case all words for better aggregation, assuming case doesn't change sentiment correlation		
			if tweeted_words.has_key(ascii_word):
				count = tweeted_words[ascii_word]['count']+1 #increment specific word count
				tweeted_words[ascii_word] = {'count':count,'frequency':count/word_count} #increase count and reset freq
			else:
				tweeted_words[ascii_word] = {'count':1,'frequency':float(1/word_count)} #initialize dictionary of tweeted word with initial count and freq
			word_count += float(1) #increase for each word in each tweet
for word in sorted(tweeted_words):
	print word + " " + str(float(tweeted_words[word]['frequency']))
