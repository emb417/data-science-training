# Twitter Sentiment Analysis
* access the twitter Application Programming Interface(API) using python
* estimate the public's perception (the sentiment) of a particular term or phrase
* analyze the relationship between location and mood based on a sample of twitter data

## Setup

### The Twitter Application Programming Interface

Twitter provides a very rich REST API for querying the system, accessing data, and control your account.

### Python 2.7.x Environment on Mac OS

1. Install Homebrew
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
1. Install Python 2
```
$ brew install python
```


* If you are new to Python, you may find it valuable to work through the codeacademy Python tutorials. In addition, many have recommended Google's Python class.

### Unicode strings

Strings in the twitter data prefixed with the letter "u" are unicode strings. For example:

```
u"This is a string"
```

Unicode is a standard for representing a much larger variety of characters beyond the roman alphabet (greek, russian, mathematical symbols, logograms from non-phonetic writing systems such as kanji, etc.)

In most circumstances, you will be able to use a unicode object just like a string.

If you encounter an error involving printing unicode, you can use the encode method to properly print the international characters, like this:

```
unicode_string = u"aaaàçççñññ"
encoded_string = unicode_string.encode('utf-8')
print encoded_string
```

### Get Twitter Data
To access the live stream, you will need to install the oauth2 library so you can properly authenticate.

```
$ pip install oauth2
```

The steps below will help you set up your twitter account to be able to access the live 1% stream.

1. Create a twitter account if you do not already have one
1. Go to https://dev.twitter.com/apps and log in with your twitter credentials
1. Click "Create New App"
1. Fill out the form and agree to the terms
1. Put in a dummy website if you don't have one you want to use
1. At this point you will be prompted to attach a mobile phone number to your account if you have not previously done so.
1. Follow the instructions at the link provided
1. On the next page, click the "Keys and Access Tokens" tab along the top, then scroll all the way down until you see the section "Your Access Token"
1. Click the button "Create My Access Token"
1. You will now copy four values into the file twitterstream.py
  * "Consumer Key (API Key)"
  * "Consumer Secret (API Secret)"
  * "Access token"
  * "Access token secret"
1. Open twitterstream.py and set the variables corresponding to the api key, api secret, access token, and access secret

You will see code like the below:

```
api_key = "<Enter api key>"
api_secret = "<Enter api secret>"
access_token_key = "<Enter your access token key here>"
access_token_secret = "<Enter your access token secret here>"
```

Now that your keys are ready, you are ready to test your access.

Run the following and make sure you see data flowing and that no errors occur.

```
$ python twitterstream.py > output.txt
```

This command pipes the output to a file. Stop the program with Ctrl-C, but wait a few minutes for data to accumulate.

If you wish, modify the file to use the twitter search API to search for specific terms. For example, to search for the term "microsoft", you can pass the following url to the twitterreq function: https://api.twitter.com/1.1/search/tweets.json?q=microsoft

## Exercises

### Derive the sentiment of each tweet

The script tweet_sentiment.py computes the sentiment of each tweet based on the sentiment scores of the terms in the tweet. The sentiment of a tweet is equivalent to the sum of the sentiment scores for each term in the tweet.

```
$ python tweet_sentiment.py AFINN-111.txt output.txt
```

The file AFINN-111.txt contains a list of pre-computed sentiment scores. Each line in the file contains a word or phrase followed by a sentiment score. Each word or phrase that is found in a tweet but not found in AFINN-111.txt should be given a sentiment score of 0. See the file AFINN-README.txt for more information.

To use the data in the AFINN-111.txt file, the script builds a dictionary.  Note that the AFINN-111.txt file format is tab-delimited, meaning that the term and the score are separated by a tab character. A tab character can be identified a "\t".

The following snippet builds the dictionary:

```
afinnfile = open("AFINN-111.txt")
scores = {} # initialize an empty dictionary
for line in afinnfile:
  term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
  scores[term] = int(score)  # Convert the score to an integer.

# print scores.items() # Print every (term, score) pair in the dictionary
```

Each line of output.txt represents a streaming message. Most, but not all, will be tweets.

It is straightforward to convert a JSON string into a Python data structure; there is a library to do so called json.

The json library is added to the top of tweet_sentiment.py

```
import json
```

Then, to parse the data in output.txt, json.loads is applied to every line in the file.

```
for line in outputfile:
	tweets.append(json.loads(line)) # builds list by formatting lines from output file
```

This function will parse the json data and return a python data stucture; in this case, it returns a dictionary. If needed, take a moment to read the documentation for Python dictionaries.

You can read the Twitter documentation to understand what information each tweet contains and how to access it, but it's not too difficult to deduce the structure by direct inspection.

### Derive the sentiment of new terms

There is a script term_sentiment.py that computes the sentiment for the terms that do not appear in the file AFINN-111.txt.

Here's how you might think about the problem: We know we can use the sentiment-carrying words in AFINN-111.txt to deduce the overall sentiment of a tweet. Once you deduce the sentiment of a tweet, you can work backwards to deduce the sentiment of the non-sentiment carrying words that do not appear in AFINN-111.txt. For example, if the word soccer always appears in proximity with positive words like great and fun, then we can deduce that the term soccer itself carries a positive sentiment.

```
$ python term_sentiment.py AFINN-111.txt output.txt
```

This script should print output to stdout. Each line of output should contain a term, followed by a space, followed by the sentiment. That is, each line should be in the format <term:string> <sentiment:float>

For example, if you have the pair ("foo", 103.256) in Python, it should appear in the output as:

```
foo 103.256
```

### Compute Term Frequency

The Python script frequency.py computes the term frequency histogram of the livestream data you harvested.

The frequency of a term can be calculated as [# of occurrences of the term in all tweets]/[# of occurrences of all terms in all tweets]

```
$ python frequency.py <tweet_file>
```

The tweet file contains data formatted the same way as the livestream data.

The script should print output to stdout. Each line of output should contain a term, followed by a space, followed by the frequency of that term in the entire file. There should be one line per unique term in the entire file. Even if 25 tweets contain the word lol, the term lol should only appear once in your output (and the frequency will be at least 25!) Each line should be in the format <term:string> <frequency:float>

For example, if you have the pair (bar, 0.1245) in Python it should appear in the output as:

```
bar 0.1245
```

### Which State is happiest?

The Python script happiest_state.py returns the name of the happiest state as a string.

The script happiest_state.py should take a file of tweets as input. It will be called from the command line like this:

```
$ python happiest_state.py <sentiment_file> <tweet_file>
```

The file AFINN-111.txt contains a list of pre-computed sentiment score.

The tweet file contains data formatted the same way as the livestream data.

There are different ways you can assign a location to a tweet.

Here are three:

1. Use the coordinates field (a part of the place object, if it exists), to geocode the tweet. This method gives the most reliable location information, but unfortunately this field is not always available and you must figure out some way of translating the coordinates into a state.
1. Use the other metadata in the place field. Much of this information is hand-entered by the twitter user and may not always be present or reliable, and may not typically contain a state name.
1. Use the user field to determine the twitter user's home city and state. This location does not necessarily correspond to the location where the tweet was posted, but it's reasonable to use it as a proxy.


* Note: Not every tweet will have a text field --- again, real data is dirty! Be prepared to debug, and feel free to throw out tweets the code can't handle to get something working. For example, you might choose to ignore all non-English tweets.

### Top ten hash tags

The Python script top_ten.py computes the ten most frequently occurring hashtags from the data.

Your script will be run from the command line like this:

```
$ python top_ten.py <tweet_file>
```

The tweet file contains data formatted the same way as the livestream data.

In the tweet file, each line is a Tweet object, as described in the twitter documentation. To find the hashtags, you should not parse the text field; the hashtags have already been extracted by twitter.

The script should print output to stdout. Each line of output should contain a hashtag, followed by a space, followed by the frequency of that hashtag in the entire file. There should be one line per unique hashtag in the entire file. Each line should be in the format <hashtag:string> <frequency:float>

For example, if you have the pair (bar, 30) in Python it should appear in the output as:

```
bar 30
```
