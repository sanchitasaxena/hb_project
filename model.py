from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()


class TwitterAndNews(db.Model):
    """ Table that stores the twitter and news trending topic string,
    timestamp, and source (twitter|news). """

    __tablename__ = "trending"

    twitter_news_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    string = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(20), nullable=False)



class ArticleAssociation(db.Model):
    """ Table that stores article title and article link. """

    __tablename__ = "articles"

    article_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    topic_string = db.Column(db.String(500), nullable=False)
    article_title = db.Column(db.String(500), nullable=False)
    article_link = db.Column(db.String(500), nullable=False)



def example_data():
    """Create some sample data."""

    TwitterAndNews.query.delete()
    ArticleAssociation.query.delete()

    # sample twitter and news topics

    tweet_one = TwitterAndNews(timestamp='2016-08-27 18:09:58.921413', string="phelps", source="twitter")
    tweet_two = TwitterAndNews(timestamp='2016-08-27 18:09:58.921413', string="kim k", source="twitter")
    news_one = TwitterAndNews(timestamp='2016-08-27 18:09:58.921413', string="trump", source="news")
    news_two = TwitterAndNews(timestamp='2016-08-27 18:09:58.921413', string="hurricane", source="news")

    # sample articles for each of the topics
    article_one = ArticleAssociation(topic_string="phelps", article_title="gold medal", article_link="www.olympics.com")
    article_two = ArticleAssociation(topic_string="phelps", article_title="best swimmer ever", article_link="www.swimmer.com")
    article_three = ArticleAssociation(topic_string="phelps", article_title="best athlete", article_link="www.swimmingiscool.com")
    article_four = ArticleAssociation(topic_string="kim k", article_title="kim and kanye", article_link="www.kardashians.com")
    article_five = ArticleAssociation(topic_string="trump", article_title="trumpinmexico", article_link="www.cnn.com")
    article_six = ArticleAssociation(topic_string="trump", article_title="trump is racist", article_link="www.huffingtonpost.com")
    article_seven = ArticleAssociation(topic_string="trump", article_title="trump is winning", article_link="www.vote4trump.com")
    article_eight = ArticleAssociation(topic_string="hurricane", article_title="hurricane katrina", article_link="www.nbc.com")
    article_nine = ArticleAssociation(topic_string="hurricane", article_title="many homeless post katrina", article_link="www.fema.com")

    db.session.add_all([tweet_one, tweet_two, news_one, news_two,
                        article_one, article_two, article_three,
                        article_four, article_five, article_six,
                        article_seven, article_eight, article_nine])
    db.session.commit()



################################################################################


def connect_to_db(app, db_uri='postgresql:///trends'):
    """Connect the database to our Flask app."""

    # Configure to use our database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # able to work with the database directly
    from server import app
    connect_to_db(app)
    print "Connected to DB."
