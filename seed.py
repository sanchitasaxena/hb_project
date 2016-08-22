from model import connect_to_db, db, TwitterAndNews, ArticleAssociation, LastRefresh
import helper_functions

from server import app
from sqlalchemy import fun

import requests
import os
import json



#create a function that saves the API query results

def save_trending():


def save_articles():











if __name__ == '__main__': 

    connect_to_db(app)
    # db.create_all()
  