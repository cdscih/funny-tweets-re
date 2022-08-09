import os
import json
import logging

from requests_oauthlib import OAuth1Session

logger = logging.getLogger(__name__)


class Twitter:
    def __init__(
        self,
        user_id: str,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ):
        self.user_id = user_id
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def get_tweets_from_followers(self):
        ...

    def get_tweets_from_liked(self):
        ...

    def get_tweets_from_mentions(self):
        ...

    def post_retweet(self, tweet_id: str):

        payload = {"tweet_id": tweet_id}

        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )

        res = oauth.post(
            f"https://api.twitter.com/2/users/{self.user_id}/retweets", json=payload
        )

        if res.status_code != 200:
            err_msg = f"Request returned an error: {res.status_code} {res.text}"
            logger.error(err_msg)
            raise Exception(err_msg)

        logger.info(f"Response code: {res.status_code}")
