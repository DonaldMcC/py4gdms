# Chap02/twitter_client.py
import os
import sys
import pprint
try:
    import tweepy
    from tweepy import API, Client, OAuthHandler, TweepyException
except ImportError:
    print('Tweepy not installed - tweets will not work')

from py4web import URL
# below line less than ideal as then can't run this file without relative import no known parent issue
# however can probably still just call tweet_test from some sort of test controller and keep going
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


def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret):
    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def publish(questiontext, filename=None):
    # The posting currently has a url to the question and the question text.  Tending to now think
    # adding a second url if we have one in the question is confusing - think we ARE Ok to add a media ID
    # if we have content on the question and that probably does make for better experience on twitter -
    # so we go with this approach for now

    try:
        consumer_key = settings.NDSPOST_API_KEY
        consumer_secret = settings.NDSPOST_API_KEY_SECRET
        access_token = settings.NDSPOST_ACCESS_TOKEN
        access_secret = settings.NDSPOST_ACCESS_TOKEN_SECRET
    except KeyError:
        sys.stderr.write("TWITTER_* environment variables not set\n")
        sys.exit(1)

    client = Client(consumer_key=consumer_key, consumer_secret=consumer_secret,
                    access_token=access_token, access_token_secret=access_secret)

    # api = get_twitter_client()
    # TODO - will only ever be one media ID for now but eventually could be a list perhaps
    # TODO think of error handling for this
    media_ids = None
    long_text = f"{quetiontext[:277]}..." if len(questiontext) > 280 else questiontext

    if filename:
        api = get_twitter_conn_v1(consumer_key, consumer_secret, access_token, access_secret)
        media = api.media_upload(filename=filename)
        # print("MEDIA: ", media)
        media_ids = [media.media_id_string]
    try:
        # seems was still on v1 endpoint now changed and simplified for now
        # result = api.create_tweet(text=short_text, full_text=long_text, media_ids=media_ids, tweet_mode="extended")
        result = client.create_tweet(text=long_text, media_ids=media_ids)
        print("TWEET: ", long_text)
        print("RESULT:", result)
    except TweepyException as e:
        print("Error occurred: ", e)
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

def tweet_test():
    questurl = URL('question/viewquest', str(1), scheme='https')
    quest_text = 'This is a test tweet'
    pub_result = publish(f'{questurl} {quest_text}')
    pprint(pub_result)
