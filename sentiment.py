import requests
import urllib
import pprint
import json
import tweepy
from soup import *

####################################################################
###     These four values compromise the API key for Twitter.  	 ###
###  The Tweepy library helps to authorize requests. Any Twitter ###
###       request can be made by calling api.API_METHOD. 		 ###
twitter_key = "RkhfsTI6trPNjwUJf2OGbJdpC"
twitter_secret = "1mdqEKXJsorxkCttpCAdyzZK8rAOE9Nnnb4shkYsmqNM7I9s00"
twitter_AT = '218404747-j6uKK8cnOQV0c65I1d5pNdLCtWeLosEonTPCDzw0'
twitter_ATS = '6xdnAxGtHeyCG255A4Y2ohs3cpNyRYBzra7nZLq4J92AR'
######################################################################

sentiment_api_key = "a6d1cff653b699d1de2cc0ecbd98f5f28549c7d3"
request_count = 0


def default():
    """ Default method for returning sentiment of the day.
            Returns the sentiment of 20 tweets averaged between searches for
            bitcoin and bitcoin news. Combines with sentiment from front page
            Google News search for bitcoin within the past 24 hours (20+ entries).
    """
    bitcoin = getTweetSentiment()
    bitcoinNews = getTweetSentiment(subject='bitcoin news')
    googleFeels = getGoogleSentiment(True)  # CHANGE TO TRUE FOR REAL SCRAPING
#   How to scale google news up?
    return (bitcoin + bitcoinNews + googleFeels) / 3


def getSentiment(msg, encode=True):
    """ Returns the numerical sentiment of MSG, [-1, 1] using an external
            Tweet API. The JSON response is first stored in a library.
            Tweets must first be encoded before being evaluated.
    """
    global request_count
    if encode:
        text = urllib.quote_plus(msg.encode('utf-8'))
    else:
        text = urllib.quote_plus(msg)
    url = "https://www.tweetsentimentapi.com/api/?key=%s&text=%s" % (
        sentiment_api_key, text)
    r = requests.get(url)
    j = r.json()
    score = j['score']
    request_count = j['request_count']
    return score

############
#  TWEETS  #
############

auth = tweepy.OAuthHandler(twitter_key, twitter_secret)
auth.set_access_token(twitter_AT, twitter_ATS)
api = tweepy.API(auth)


def getTweetSentiment(n=10, subject='bitcoin', language='en', rtype='popular'):
    """ Returns the average sentiment about Bitcoins using the n most recent
            and popular Tweets on Twitter using the search criteria SUBJECT.
    """
    tweets = tweepy.Cursor(api.search, q=subject, count=n, result_type=rtype, lang=language).items(n)
    total_sentiment = 0.0
    for t in tweets:
        sentiment = getSentiment(t.text)
        total_sentiment += sentiment
        print t.text + "\nSentiment = " + str(sentiment)
    avg_sentiment = total_sentiment / float(n)
    return avg_sentiment


def printTweet(tweets):
    """ Given a list of tweets from an API search, prints the text of each
            seperated by new lines.
    """
    x = 0
    for t in tweets:
        print t.text
        x += 1
    print str(x) + " tweets."

############
#  GOOGLE  #
############


def getGoogleSentiment(fromFile=True):
    """ Returns the sentiment about Bitcoins using a Google News search. 
            In order to scrape new data from Google, fromFile must be False.
    """
    if fromFile:
        soup = getSoupFromFile()
    else:
        soup = getSoup()
    total_sentiment = 0.0
    headlines = getHeadlines(soup)
    subheadlines = getSubHeadlines(soup)
    subtext = getSubText(soup)
    for line in headlines:
        sentiment = getSentiment(line, False)
        total_sentiment += sentiment
        print line + "\nSentiment = " + str(sentiment)
    for line in subheadlines:
        sentiment = getSentiment(line, False)
        total_sentiment += sentiment
        print line + "\nSentiment = " + str(sentiment)
    for line in subtext:
        sentiment = getSentiment(line, False)
        total_sentiment += sentiment
        print line + "\nSentiment = " + str(sentiment)
    size = float(len(headlines) + len(subheadlines) + len(subtext))
    avg_sentiment = total_sentiment / size
    return avg_sentiment
