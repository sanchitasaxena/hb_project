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
    topic_string = db.Column(db.String, nullable=False)
    article_title = db.Column(db.String(300), nullable=False)
    # changed the string length from 500 to 1000 characters... hope this works
    article_link = db.Column(db.String(500), nullable=False)






################################################################################


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///trends'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # able to work with the database directly
    from server import app
    connect_to_db(app)
    print "Connected to DB."

