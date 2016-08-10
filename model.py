from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


class User(db.Model):
    """User table."""

    __tablename__ = "users"




class UserTopic(db.Model):
    """User ratings on trending topics."""

    __tablename__ = "ratings"



class Topic(db.Model):
    """Trending topics database."""

    __tablename__ = "topics"




