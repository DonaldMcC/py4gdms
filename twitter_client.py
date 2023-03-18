# Chap02/twitter_client.py
import os
import sys
from tweepy import API
from tweepy import OAuthHandler
import tweepy
from . import settings


def get_twitter_auth():
    """Setup Twitter authentication.

    Return: tweepy.OAuthHandler object
    """
    # try:
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


def publish(questiontext, filename=None):
    # The posting currently has a url to the question and the question text.  Tending to now think
    # adding a second url if we have one in the question is confusing - think we ARE Ok to add a media ID
    # if we have content on the question and that probably does make for better experience on twitter -
    # so we go with this approach for now
    api = get_twitter_client()
    # TODO - will only ever be one media ID for now but eventually could be a list perhaps
    # TODO think of error handling for this
    media_ids = None

    if filename:
        media = api.media_upload(filename=filename)
        print("MEDIA: ", media)
        media_ids = [media.media_id_string]
        #tweet = api.update_status(status="Image upload", media_ids=
        #[media.media_id_string])
    try:
        result = api.update_status(questiontext, full_text=questiontext, media_ids=media_ids, tweet_mode="extended")
        print("TWEET: ", e)
    except tweepy.errors as e:
        print("Eror occurred: ", e)
        result = e
    return result


"""
    This seems to be simple example of updating with media - probalby have a look at url's too and 
    see how they go together - seems urls just go into the text if required and then get auto shortened I think
    
    https: // stackoverflow.com / questions / 70891698 / how - to - post - a - tweet -
    with-media - picture - using - twitter - api - v2 - and -tweepy - python

    media = api.media_upload(filename="./assets/twitter-logo.png")
    print("MEDIA: ", media)

    tweet = api.update_status(status="Image upload", media_ids=
    [media.media_id_string])
    print("TWEET: ", tweet)
    
"""
