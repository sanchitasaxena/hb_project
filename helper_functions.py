import os
import sys
import twitter
import requests
import json

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




#calling the bing_search() function to get the top 10 trending news topics
#bing_search()
#calling the DisplayTrends(trends) function to get the top trending tweets
#display_trends(trends)

#trends = api.GetTrendsCurrent()
#trends
#type(trends)
#type(trends[0])

#dir(trends[0])
#['AsDict', 'AsJsonString', 'NewFromJsonDict', 'events', 'name',
#'param_defaults', 'promoted_content', 'query', 'timestamp', 'url', 'volume']
