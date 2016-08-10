import os
import sys
import twitter
import requests
import json

API_KEY = os.environ.get("BING_KEY_ONE")

api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

def GetTrendsCurrent(self, exclude=None):
        """Get the current top trending topics (global)

        Args:
          exclude:
            Appends the exclude parameter as a request parameter.
            Currently only exclude=hashtags is supported. [Optional]

        Returns:
          A list with 10 entries. Each entry contains a trend.
        """

        #this output is of a list of tuples with the format
        #[Trend(Name=u'#LevantamientoDePesas', Time=2016-08-08T23:55:44Z, URL=http://), ...]
        return self.GetTrendsWoeid(woeid=1, exclude=exclude)

trends = api.GetTrendsCurrent()

def DisplayTrends(trends):
    #setting the input to the list returned from GetTrendsCurrent()
    #trends = api.GetTrendsCurrent()
    #for the list of objects trends, provide the name and url attribute to the
    for trend in trends:
        #apply jinja eventuall so that each name has the URL as it's name...
        print trend.name, trend.url


#trends = api.GetTrendsCurrent()
#trends
#type(trends)
#type(trends[0])

#dir(trends[0])
#['AsDict', 'AsJsonString', 'NewFromJsonDict', 'events', 'name', 
#'param_defaults', 'promoted_content', 'query', 'timestamp', 'url', 'volume']


def bing_search():
    headers = {'Ocp-Apim-Subscription-Key': API_KEY }
    r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/trendingtopics', headers=headers)
    results = json.loads(r.content)
    for i in range(10):
        topic = results['value'][i]['name']
        topic_url = results['value'][i]['webSearchUrl']

        print topic, topic_url

#calling the bing_search() function to get the top 10 trending news topics
bing_search()
#calling the DisplayTrends(trends) function to get the top trending tweets
DisplayTrends(trends)
