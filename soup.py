from bs4 import BeautifulSoup
import sys
import urllib2

filename = "Data/bitcoinnews.html"


def getSoup():
    """ Returns some soup of the Google News search for Bitcoin in the
            past 24 hrs. A new 'bitcoinnews.html file is downloaded each
            time this function is called which is used to generate the
            soup.

            A webscraping strategy is required because an API for Google
            News no longer exists. Instead, a request is issued with the 
            designated user_agent, which makes the program appear human. 

            Limit requests to less than 1 per minute or fewer to avoid
            Google's wrath.
    """

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    url = "https://www.google.com/search?hl=en&gl=us&tbm=nws&authuser=0&q=bitcoin&oq=bitcoin&gs_l=news-cc.3...2004.2368.0.2554.0.0.0.0.0.0.0.0..0.0...0.0...1ac.1.#q=bitcoin&hl=en&gl=us&authuser=0&tbm=nws&tbs=qdr:d"
    headers = {'User-Agent': user_agent, }
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request)

    output = open('Data/bitcoinnews.html', 'wb')
    output.write(response.read())
    output.close()

    return BeautifulSoup(open("Data/bitcoinnews.html"))


def getSoupFromFile():
    """ Returns a soup from the archived file, not from Google itself."""
    return BeautifulSoup(open(filename))


def getHeadlines(soup):
    """ Returns all the headlines from the webpage as a list of strings."""

    headlines = soup.findAll("div", {"class": "_cnc"})
    myList = []
    s = ''
    for h in headlines:
        for item in h.a:
            if item.encode('utf-8')[0] != '<':
                s += item.encode('utf-8')
            else:
                s += "BTC"
        myList.append(s)
        s = ''
    return myList


def getSubHeadlines(soup):
    """ Returns all the subheadlines from the webpage as a list of strings."""
    subheadlines = soup.findAll("div", {"class": "_hnc card-section"})
    myList = []
    s = ''
    for sh in subheadlines:
        for item in sh.a:
            if item.encode('utf-8')[0] != '<':
                s += item.encode('utf-8')
            else:
                s += "BTC"
        myList.append(s)
        s = ''
    return myList


def getSubText(soup):
    """ Returns all the subheadlines from the webpage as a list of strings."""
    subtext = soup.findAll("div", {"class": "st"})
    myList = []
    s = ''
    for sub in subtext:
        for item in sub.contents:
            text = item.encode('utf-8')
            if text[0] != '<':
                if text[-3:] == '...':
                    text = text[:-3]
                s += text
            else:
                s += "BTC".encode('utf-8')
        myList.append(s)
        s = ''
    return myList


def printSomeShit(soup):
    """ Given a soup of the Google News Page for BTC, print some shit."""

    print "******** BITCOIN HEADLINES ********"
    for h in getHeadlines(soup):
        print h

    print "\n******** SUBHEADLINES ********"
    for sh in getSubHeadlines(soup):
        print sh

    print "\n******** MORE TEXT ********"
    for s in getSubText(soup):
        print s


def main():
    """ Default behavior: getSoup then printSomeShit."""
    printSomeShit(getSoup())


def mainFromFile():
    """ Just grabs the existing HTML file to parse and print."""
    printSomeShit(getSoupFromFile())


# Backup: Feedzilla api for getting news headlines, just make sure to use
# the right date.

# >>> url = "http://api.feedzilla.com/v1/articles/search.json?q=bitcoin&since=2015-01-03"
# >>> import requests
# >>> r = requests.get(url)
# >>> j = r.json()
# >>> a = j['articles']
# >>> for i in a:
# ...     print i['title'], i['summary']
