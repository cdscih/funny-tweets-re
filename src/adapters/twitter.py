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
        owner_user_id: str,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ):
        self.owner_user_id = owner_user_id

        self.oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

        try:
            self.user = self._get_bot_user()
            logging.info(f"User {self.user.username} set as bot account")
        except Exception as err:
            raise ValueError("Twitter credentials missing or invalid.")

    def _get_bot_user(self) -> User:
        res = self.oauth.get(
            "https://api.twitter.com/2/users/me?user.fields=public_metrics",
        ).json()["data"]
        return User(
            **{
                "id": res["id"],
                "name": res["name"],
                "username": res["username"],
                "followers_count": res["public_metrics"]["followers_count"],
            }
        )

    def get_followed_users_list(self) -> list[User]:
        logger.info(f"Retrieving list of users followed by the bot")
        res = self.oauth.get(
            f"https://api.twitter.com/2/users/{self.user.id}/following?user.fields=public_metrics"
        )
        if res.status_code != 200:
            raise Exception(f"Request returned an error: {res.status_code} {res.text}")
        return [
            User(
                **{
                    "id": user["id"],
                    "name": user["name"],
                    "username": user["username"],
                    "followers_count": user["public_metrics"]["followers_count"],
                }
            )
            for user in res.json()["data"]
        ]

    def get_recent_tweets(self, user: User) -> list[Tweet]:
        logger.info(f"Retrieving tweets of user {user.username}")
        res = self.oauth.get(
            f"https://api.twitter.com/2/users/{user.id}/tweets?expansions=author_id&tweet.fields=public_metrics"
        )
        if res.status_code != 200:
            logger.error(f"Request returned an error: {res.status_code} {res.text}")
            return []
        return [
            Tweet(
                **{
                    "id": tweet["id"],
                    "author_id": tweet["author_id"],
                    "like_count": tweet["public_metrics"]["like_count"],
                }
            )
            for tweet in res.json()["data"]
        ]

    def get_tweets_from_liked(self) -> tuple[list[Tweet], list[User]]:
        logger.info("Retrieving tweets liked from the bot")
        res = self.oauth.get(
            f"https://api.twitter.com/2/users/{self.user.id}/liked_tweets?expansions=author_id&tweet.fields=public_metrics&user.fields=public_metrics"
        )
        if res.status_code != 200:
            logger.error(f"Request returned an error: {res.status_code} {res.text}")
            return []

        res_data = res.json()

        tweets = [
            Tweet(
                **{
                    "id": tweet["id"],
                    "author_id": tweet["author_id"],
                    "like_count": tweet["public_metrics"]["like_count"],
                }
            )
            for tweet in res_data["data"]
        ]

        users = [
            User(
                **{
                    "id": user["id"],
                    "name": user["name"],
                    "username": user["username"],
                    "followers_count": user["public_metrics"]["followers_count"],
                }
            )
            for user in res_data["includes"]["users"]
        ]

        return tweets, users

    def get_tweets_from_owner_mentions(self) -> tuple[list[Tweet], list[User]]:
        logger.info("Retrieving tweets from the owner's mentions of the bot")
        params = {"query": f"from:{self.owner_user_id} @{self.user.username} is:reply"}
        res = self.oauth.get(
            f"https://api.twitter.com/2/tweets/search/recent?tweet.fields=author_id,public_metrics&expansions=referenced_tweets.id,referenced_tweets.id.author_id&user.fields=public_metrics",
            params=params,
        )
        if res.status_code != 200:
            logger.error(f"Request returned an error: {res.status_code} {res.text}")
            return []

        res_data = res.json()["includes"]

        tweets = [
            Tweet(
                **{
                    "id": tweet["id"],
                    "author_id": tweet["author_id"],
                    "like_count": tweet["public_metrics"]["like_count"],
                }
            )
            for tweet in res_data["tweets"]
        ]

        users = [
            User(
                **{
                    "id": user["id"],
                    "name": user["name"],
                    "username": user["username"],
                    "followers_count": user["public_metrics"]["followers_count"],
                }
            )
            for user in res_data["users"]
        ]

        return tweets, users

    def post_retweet(self, tweet_id: str):
        logger.info(f"Posting retweet for tweet {tweet_id}")
        res = self.oauth.post(
            f"https://api.twitter.com/2/users/{self.user.id}/retweets",
            json={"tweet_id": tweet_id},
        )
        if res.status_code != 200:
            err_msg = f"Request returned an error: {res.status_code} {res.text}"
            logger.error(err_msg)
            raise Exception(err_msg)
        logger.info(f"Successfully retweeted {tweet_id}")
