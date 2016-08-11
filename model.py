from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()

#user class to create table of users (for sprint 2)
class User(db.Model):
    """User table."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    first_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<User user_id=%s email=%s>" % (self.user_id,
    #                                            self.email)



#rating model for ratings table (for sprint 2)
class Rating(db.Model):
    """User ratings on trending topics."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    topic_id = db.Column(db.Integer,
                         db.ForeignKey('topics.topic_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("ratings",
                                              order_by=rating_id))

    # Define relationship to topic
    topic = db.relationship("Topic",
                            backref=db.backref("ratings",
                                               order_by=rating_id))

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     s = "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>"
    #     return s % (self.rating_id, self.topic_id, self.user_id,
    #                 self.score)


#topic model for topics table (for sprint 1) bc topics can be stored without
#ratings

# class Topic(db.Model):
#     """Trending topics database."""

#     __tablename__ = "topics"

#     topic_id = db.Column(db.Integer,
#                          autoincrement=True,
#                          primary_key=True)
#     name = db.Column(db.String(100))
#     link = db.Column(db.String(200))

#     # def __repr__(self):
#     #     """Provide helpful representation when printed."""

#     #     return "<Topic topic_id=%s name=%s>" % (self.topic_id,
#     #                                              self.name)

class Tweet(db.Model):
    """Trending topics database."""

    __tablename__ = "tweets"

    tweet_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    name = db.Column(db.String(100))
    link = db.Column(db.String(200))

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<Topic topic_id=%s name=%s>" % (self.article_id,
    #                                              self.name)

class Article(db.Model):
    """Trending topics database."""

    __tablename__ = "articles"

    article_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    name = db.Column(db.String(100))
    link = db.Column(db.String(200))

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<Topic topic_id=%s name=%s>" % (self.article_id,
    #                                              self.name)



#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
