from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, TwitterAndNews, ArticleAssociation
from helper_functions import *
from datetime import datetime
import string

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

####################LOG IN / LOG OUT / REGISTRATION HANDLING####################
@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/feed')
def feed():
    """Takes you to page that displays the feed."""

    last_refresh = db.session.query(TwitterAndNews.timestamp).order_by(TwitterAndNews.timestamp.desc()).first()[0]

    if (datetime.now() - last_refresh).seconds > 3600:
        save_trends_to_database()
        save_articles_to_database()
        last_refresh = db.session.query(TwitterAndNews.timestamp).order_by(TwitterAndNews.timestamp.desc()).first()[0]

    tweets = TwitterAndNews.query.filter_by(timestamp=last_refresh, source='twitter').all()
    news_trends = TwitterAndNews.query.filter_by(timestamp=last_refresh, source='news').all()


    #create a dictionary to store the articles for each topic
    twitter_with_articles = {}

    for tweet in tweets:
        tweet_articles = db.session.query(ArticleAssociation).filter(ArticleAssociation.topic_string == tweet.string).all()

        tweet_article_info = []

        for item in tweet_articles:
            tweet_article_info.append({"title": item.article_title, "url": item.article_link})

        twitter_with_articles[tweet.string] = tweet_article_info

    news_with_articles = {}

    for news in news_trends:
        news_articles = db.session.query(ArticleAssociation).filter(ArticleAssociation.topic_string == news.string).all()
        
        news_article_info = []

        for article in news_articles:
            news_article_info.append({"title": article.article_title, "url": article.article_link})

        news_with_articles[news.string] = news_article_info

        # shared_topics


    # tweet_words = tweet.string.split(' ')

    #are any of the words in here in the tweet -- percentage (50%) same then related

  

    # compare two strings and return a description regarding similarities

    news_words = []
    for news in news_trends:
        news_word_list = news.string.split(' ')
        for n in news_word_list:
            for c in string.punctuation:
                n = n.replace(c,'')
            news_words.append(n)
    print news_words


    tweet_words = []
    for tweet in tweets:
        whole_tweet = tweet.string
        for c in string.punctuation:
            tweet_word = whole_tweet.replace(c,'')
        tweet_words.append(tweet_word)
    print tweet_words

    shared_topics = []   
    for t in tweet_words:
        for term in news_words:
            # not in ['a', 'the', 'this', 'are', 'and', 'it'] and
            if term in t:
                shared_topics.append(term)
    
    if not shared_topics:
        print "nothing shared"


    return render_template("feed.html",
                            tweets=tweets,
                            news_trends=news_trends,
                            twitter_with_articles=twitter_with_articles,
                            news_with_articles=news_with_articles,
                            shared_topics=shared_topics)


################################################################################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
