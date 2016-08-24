from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, TwitterAndNews, ArticleAssociation
import helper_functions

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


# @app.route('/register', methods=['GET'])
# def register_form():
#     """Show form for user signup."""

#     return render_template("register_form.html")


# @app.route('/register', methods=['POST'])
# def register_process():
#     """Process registration."""

#     # # Get form variables
#     # email = request.form["email"]
#     # password = request.form["password"]
#     # first_name = request.form["first_name"]

#     # new_user = User(email=email, password=password, first_name=first_name)

#     # db.session.add(new_user)
#     # db.session.commit()

#     # flash("User %s added." % email)
#     return redirect("/")


# @app.route('/login', methods=['GET'])
# def login_form():
#     """Show login form."""

#     return render_template("login_form.html")


# @app.route('/login', methods=['POST'])
# def login_process():
#     """Process login."""

#     # # Get form variables
#     # email = request.form["email"]
#     # password = request.form["password"]

#     # user = User.query.filter_by(email=email).first()

#     # if not user:
#     #     flash("No such user")
#     #     return redirect("/login")

#     # if user.password != password:
#     #     flash("Incorrect password")
#     #     return redirect("/login")

#     # session["user_id"] = user.user_id

#     # flash("Logged in")
#     return redirect("/users/%s" % user.user_id)


# @app.route('/logout')
# def logout():
#     # """Log out."""

#     # del session["user_id"]
#     # flash("Logged Out.")
#     return redirect("/")
#################################FEED HANDLING##################################

@app.route('/feed')
def feed(timestamp):
    """Takes you to page that displays the feed."""


    # Query's DB to get things based on the datetime timestamp

    # fetches the trending tweet strings and their articles.
    tweets = TwitterAndNews.query.filter_by(timestamp=timestamp, source='twitter').all()

    news_trends = TwitterAndNews.query.filter(timestamp=timestamp, source='news').all()


    tweet_search_articles = ArticleAssociation(twitter_news_id=twitter_news_id).all()
    #how would I be able to get the articles for the news and articles for tweets?
    news_search_articles = ArticleAssociation(twitter_news_id=twitter_news_id).all()

    # # gets the top trending tweets
    # tweets = helper_functions.display_trends()
    # print tweets

    # tweet_search_articles = helper_functions.create_twitter_topics_trending()

    # print tweet_search_articles

    # # gets the top trending articles
    # news_trends = helper_functions.create_twitter_topics_trending()
    # print news_trends

    # news_search_articles = helper_functions.create_news_topics_trending
    # print news_search_articles

    return render_template("feed.html",
                            tweets=tweets,
                            news_trends=news_trends,
                            tweet_search_articles=tweet_search_articles,
                            news_search_articles=news_search_articles)


################################################################################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
