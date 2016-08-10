import requests
import json

def bing_search():
    headers = {'Ocp-Apim-Subscription-Key': 'c4f7341ec10a42da873a5b1c84f24b9b'}
    r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/trendingtopics', headers=headers)
    results = json.loads(r.content)
    for i in range(10):
        topic = results['value'][i]['name']
        topic_url = results['value'][i]['webSearchUrl']

        print topic, topic_url


bing_search()









    #search_result.keys()



# [u'_type', u'value']

# d['value'][0]

# d['value'][0].keys()
#[u'isBreakingNews', u'webSearchUrl', u'image', u'name', u'query']

#d['value'][0]['name'], d['value'][0]['webSearchUrl']

#u'Sports betting denied'

#d['value'][0]['webSearchUrl']

#u'https://www.bing.com/cr?IG=81973BB....... etc
# r = bing_search()