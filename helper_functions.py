import os
import sys
import twitter
import requests
import json

from datetime import datetime

from model import TwitterAndNews, ArticleAssociation, db, connect_to_db
from server import *



API_KEY = os.environ.get("BING_KEY_TWO")

api = twitter.Api(
        consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
        access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
        access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

def GetTrendsWoeid(self, woeid=23424977, exclude=None):
    """Return the top 10 trending topics for a specific WOEID, if trending
    information is available for it.
    Args:
      woeid:
        the Yahoo! Where On Earth ID for a location.
      exclude:
        Appends the exclude parameter as a request parameter.
        Currently only exclude=hashtags is supported. [Optional]
    Returns:
      A list with 10 entries. Each entry contains a trend.
    """
    url = '%s/trends/place.json' % (self.base_url)
    parameters = {'id': woeid}

    if exclude:
        parameters['exclude'] = exclude

    resp = self._RequestUrl(url, verb='GET', data=parameters)
    data = self._ParseAndCheckTwitter(resp.content.decode('utf-8'))
    trends = []
    timestamp = data[0]['as_of']

    for trend in data[0]['trends']:
        trends.append(Trend.NewFromJsonDict(trend, timestamp=timestamp))
    return trends
    
def display_trends():
    """ Returns the top ten trending tweets in the United States as a list of
        tuples containing the tweet's name and tweet's URL.
    """
    #setting the input to the list returned from GetTrendsCurrent()
    trends = api.GetTrendsWoeid(woeid=23424977, exclude=None)
    #for the list of objects trends, provide the name and url attribute to the
    top_tweets = []
    for trend in trends:
        top_tweets.append((trend.name, trend.url))
    top_tweets = top_tweets[:5]
    return top_tweets


def bing_search():
    """ Returns the top ten trending news searches in the United States as a list of
        tuples containing the search's name and search's URL on bing.
    """
    headers = {'Ocp-Apim-Subscription-Key': API_KEY}
    r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/trendingtopics', headers=headers)
    results = json.loads(r.content)
    articles = []
    for i in range(5):
        topic = results['value'][i]['name']
        topic_url = results['value'][i]['webSearchUrl']
        articles.append((topic, topic_url))
    return articles


def bing_search_based_on_query(search):
    """ Returns the top ten trending tweets in the United States as a list of
    tuples containing the tweet's name and tweet's URL.
    """
    headers = {'Ocp-Apim-Subscription-Key': API_KEY}
    payload = {'q': search}

    r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/search', params=payload, headers=headers)
    search_results = json.loads(r.content)
    # open file, pass the json dictionary

    # search_results = open(search)

    search_articles = []
    # if we got results, add them to the dictionary, else keep the list empty
    if search_results['value']:
        for i in range(len(search_results['value'])):
            article_name = search_results['value'][i]['name']
            article_url = search_results['value'][i]['url']
            search_articles.append((article_name, article_url))
    # search_results.close()

    return search_articles



def get_topic_articles(topics_trending):
    """ Takes the top trending tweet topics and bing searches, passes them as
        lists (one for bing, one for twitter), and uses the items in the lists
        as keys and their articles (from the function bing_search_based_on_query)
        as values in a dictionary. This function will be called in server.py
        so the article name and url can be displayed on feed.html.

        Corrusponding articles for each topic whether it be twitter or news.
    """
    # creating an empty dictionary to store topics as keys and article name and
    # url as tuples
    topic_articles = {}
    # iterating over the list that's passed into the function
    for topic in topics_trending:
        # settng the topic as the key and the value as what's returend from
        # the function bing_search_based_on_query(topic)
        # ('Aricle Name', 'URL')
        topic_articles[topic] = bing_search_based_on_query(topic)
    # returns a diciontary topic_articles = {
    #                                      'topic': [('Aricle Name', 'URL'),
    #                                                ('Aricle Name', 'URL')...]
    return topic_articles



def create_twitter_topics_trending():

    tweets = display_trends()
    # empty list to store trending tweet names
    tweet_search = []
    # iterating over the list of tuples of tweets and urls
    for tweet in tweets:
        # adding the tuple names to the empty list
         tweet_search.append(tweet[0])

    # calls the function that creates a dictionary using the list as keys,
    # making the values of the dictionaries the search results (a list of
    # article names and their urls)
    tweet_search_articles = get_topic_articles(tweet_search)

    return tweet_search_articles

def create_news_topics_trending():

    news_trends = bing_search()
    # empty list to store article names for search
    news_search = []
    # for loop that iterates through the list of tuples of articles
    for news in news_trends:
        # adds the first element in tuple (article name) to the empty list
        news_search.append(news[0])

    # calls the function that creates a dictionary using the list as keys,
    # making the values of the dictionaries the search results (a list of
    # article names and their urls)

    news_search_articles = get_topic_articles(news_search)

    return news_search_articles

#DO I EVEN NEED THIS!
def save_trends_to_database():

    # function that outputs list of tweets trending as tuples
    tweet_tuple_list = display_trends()
    timestamp = datetime.now()
    for tweet_topic in tweet_tuple_list:
        string = tweet_topic[0]
        source = 'twitter'

        adding_stuff = TwitterAndNews(timestamp=timestamp, string=string, source=source)

        db.session.add(adding_stuff)

    # function that outputs a list of the news topics trending as tuples
    news_tuple_list = bing_search()
    for news_topic in news_tuple_list:
        string = news_topic[0]
        source = 'news'

        adding_stuff = TwitterAndNews(timestamp=timestamp, string=string, source=source)

        db.session.add(adding_stuff)


    db.session.commit()

def save_articles_to_database():
    #twitter
    twitter_dictionary = create_twitter_topics_trending()

    for key, values in twitter_dictionary.items():
        for item in values:
            article_title = item[0]
            article_link = item[1]
            adding_stuff = ArticleAssociation(article_title=article_title,
                                              article_link=article_link,
                                              topic_string=key)
            db.session.add(adding_stuff)

    #news
    news_dictionary = create_news_topics_trending()

    for key, values in news_dictionary.items():
        for item in values:
            article_title = item[0]
            article_link = item[1]
            adding_stuff = ArticleAssociation(article_title=article_title,
                                              article_link=article_link,
                                              topic_string=key)
            db.session.add(adding_stuff)

    db.session.commit()



if __name__ == "__main__":
    # able to work with the database directly
    connect_to_db(app)
    print "Connected to DB."