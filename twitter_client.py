# Chap02/twitter_client.py
import os
import sys
from tweepy import API
from tweepy import OAuthHandler
from . import settings

def get_twitter_auth():
    """Setup Twitter authentication.

    Return: tweepy.OAuthHandler object
    """
    #try:
    #    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    #    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    #    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    #    access_secret = os.environ['TWITTER_ACCESS_SECRET']

    try:
        consumer_key = settings.NDSPOST_API_KEY
        consumer_secret = settings.NDSPOST_API_KEY_SECRET
        access_token = settings.NDSPOST_ACCESS_TOKEN
        access_secret = settings.NDSPOST_ACCESS_TOKEN_SECRET
    except KeyError:
        sys.stderr.write("TWITTER_* environment variables not set\n")
        sys.exit(1)    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

def get_twitter_client():
    """Setup Twitter API client.settings.py

    Return: tweepy.API object
    """
    auth = get_twitter_auth()
    client = API(auth)
    return client

def publish(questiontext):
    api = get_twitter_client()
    print('I will publish')
    print(questiontext)
    #TODO think of error handling for this
    result = api.update_status(questiontext)
    return result