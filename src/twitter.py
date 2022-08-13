import os
import json
import logging

import functools

from requests_oauthlib import OAuth1Session

from entities import User, Tweet

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
        if not all(
            [user_id, consumer_key, consumer_secret, access_token, access_token_secret]
        ):
            raise ValueError("One of the init params was empty.")

        self.user_id = user_id
        self.oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

    def get_followed_users_list(self) -> list[User]:
        return [User(id=1480156703412920327, name="claudio", username="cdscih")]
        res = self.oauth.get(
            f"https://api.twitter.com/2/users/{self.user_id}/following"
        )
        if res.status_code != 200:
            raise Exception(f"Request returned an error: {res.status_code} {res.text}")
        return [User(**user) for user in res.json()["data"]]

    def get_recent_tweets_ids(self, user: User) -> list[str]:
        logger.info(f"Retrieving tweets of user {user.username}")
        res = self.oauth.get(
            f"https://api.twitter.com/2/users/{user.id}/tweets?expansions=author_id"
        )
        if res.status_code != 200:
            logger.error(f"Request returned an error: {res.status_code} {res.text}")
            return []
        return [Tweet(**tweet) for tweet in res.json()["data"]]

    def get_tweets_ids_from_liked(self):
        ...

    def get_tweets_ids_from_mentions(self):
        ...

    def post_retweet(self, tweet_id: str):
        logger.info(f"Posting retweet for tweet {tweet_id}")
        res = self.oauth.post(
            f"https://api.twitter.com/2/users/{self.user_id}/retweets",
            json={"tweet_id": tweet_id},
        )
        if res.status_code != 200:
            err_msg = f"Request returned an error: {res.status_code} {res.text}"
            logger.error(err_msg)
            raise Exception(err_msg)
        logger.info(f"Successfully retweeted {tweet_id}")
