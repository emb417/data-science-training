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

states = {}
for tweet in tweets:
	tweet_score = 0 #track score in a tweet
	if tweet.has_key("place") \
	and tweet["place"] != None \
	and tweet["place"].has_key("country_code") \
	and tweet["place"]["country_code"] != None \
	and tweet["place"]["country_code"] == "US" \
	and tweet["place"].has_key("full_name") \
	and tweet["place"]["full_name"] != None:
		words = tweet["text"].split() #split tweet into individual words
		for word in words:
			if scores.has_key(word.encode('ascii','ignore')): #check if scores has the key, also coverting unicode to ascii for better matching
				tweet_score += scores[word.encode('ascii','ignore')] #add up score

		fn_code = tweet["place"]["full_name"].split()
		state_code = fn_code[len(fn_code)-1].encode('ascii','ignore')
		if state_code != "USA":
			if states.has_key(state_code):
				states[state_code] = states[state_code]+tweet_score
			else:
				states[state_code] = tweet_score

happiest_state = {"US":-10000}
for state in states:
	for happiest in happiest_state:
		if states[state] > happiest_state[happiest]:
			happiest_state = {state:states[state]}

for happiest in happiest_state:
	print happiest