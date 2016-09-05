import requests
from bs4 import BeautifulSoup

def get_stuff(topic):

    url = 'https://www.google.com/search?hl=en&gl=us&tbm=nws&authuser=0&q='+ str(topic) +'&oq='+ str(topic) +'&gs_l=news-cc.1.0.43j0l10j43i53.451776.453927.0.459304.14.8.0.6.6.1.197.773.4j4.8.0...0.0...1ac.1.VSlN5-ARhY0'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # links = soup.find_all("a")

    # for link in links:
    #     print "<a href='%s'>%s</a>" %(link.get("href"), link.text)

    general = soup.find_all("div", {"class":"g _cy"})

    for item in general:
        item_info = item.contents[0].find_all("div", {"class": "ts _V6c _Zmc _XO _knc _d7c"})[0].text
        print item_info
    



#get_stuff('Serena Williams')
        # print item.contents[1].find_all("p", {"class": "adr"})[0].text
        # try:
        #     print item.contents[1].find_all("span", {"itemprop": "streetAddress"})[0].text
        #     print item.contents[1].find_all("span", {"itemprop": "addressLocality"})[0].text
        #     print item.contents[1].find_all("span", {"itemprop": "addressRegion"})[0].text
        #     print item.contents[1].find_all("span", {"itemprop": "postalCode"})[0].text
        # except:
        #     pass
        # try:
        #     print item.contents[1].find_all("li", {"class": "primary"})[0].text
        # except:
        #     pass

