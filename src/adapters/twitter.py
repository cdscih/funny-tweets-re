import logging

from requests_oauthlib import OAuth1Session

from entities import User, Tweet

logger = logging.getLogger(__name__)


class InvalidCredentials(ValueError()):
    ...


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
            logging.info(f"User {self.user} set as bot account")
        except Exception as err:
            logger.error(err)
            raise InvalidCredentials("Twitter credentials missing or invalid.")

    def _get_bot_user(self) -> User:
        res = self.oauth.get(
            "https://api.twitter.com/2/users/me",
            params={"user.fields": "public_metrics"},
        )
        res.raise_for_status()

        user = res.json()["data"]

        return User(
            **{
                "id": user["id"],
                "name": user["name"],
                "username": user["username"],
                "followers_count": user["public_metrics"]["followers_count"],
            }
        )

    def get_followed_users_list(self) -> list[User]:
        logger.info("Retrieving list of users followed by the bot")

        res = self.oauth.get(
            f"https://api.twitter.com/2/users/{self.user.id}/following",
            params={"user.fields": "public_metrics"},
        )
        res.raise_for_status()

        if not res.json().get("data"):
            logger.info("No users found followed from the bot")
            return []

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
        logger.info(f"Retrieving tweets of user {user}")

        res = self.oauth.get(
            f"https://api.twitter.com/2/users/{user.id}/tweets",
            params={"expansions": "author_id", "tweet.fields": "public_metrics"},
        )
        res.raise_for_status()

        tweets = res.json().get("data")

        if not tweets:
            logger.info(f"No recent tweets found for user {user}")
            return []

        return [
            Tweet(
                **{
                    "id": tweet["id"],
                    "author_id": tweet["author_id"],
                    "like_count": tweet["public_metrics"]["like_count"],
                }
            )
            for tweet in tweets
        ]

    def get_tweets_from_liked(self) -> tuple[list[Tweet], list[User]]:
        logger.info("Retrieving tweets liked from the bot")

        res = self.oauth.get(
            f"https://api.twitter.com/2/users/{self.user.id}/liked_tweets",
            params={
                "expansions": "author_id",
                "tweet.fields": "author_id,public_metrics",
                "user.fields": "public_metrics",
            },
        )
        res.raise_for_status()

        if not res.json().get("data"):
            logger.info("No available liked tweets found")
            return [], []

        tweets = [
            Tweet(
                **{
                    "id": tweet["id"],
                    "author_id": tweet["author_id"],
                    "like_count": tweet["public_metrics"]["like_count"],
                }
            )
            for tweet in res.json()["data"]
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
            for user in res.json()["includes"]["users"]
        ]

        return tweets, users

    def get_tweets_from_owner_mentions(self) -> tuple[list[Tweet], list[User]]:
        logger.info("Retrieving tweets from the owner's mentions of the bot")

        res = self.oauth.get(
            "https://api.twitter.com/2/tweets/search/recent",
            params={
                "query": f"from:{self.owner_user_id} @{self.user.username} is:reply",
                "tweet.fields": "author_id,public_metrics",
                "user.fields": "public_metrics",
                "expansions": "referenced_tweets.id,referenced_tweets.id.author_id",
            },
        )
        res.raise_for_status()

        data = res.json().get("includes")

        if not data:
            logger.info("No available tweets found from owner mentions")
            return [], []

        tweets = [
            Tweet(
                **{
                    "id": tweet["id"],
                    "author_id": tweet["author_id"],
                    "like_count": tweet["public_metrics"]["like_count"],
                }
            )
            for tweet in data["tweets"]
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
            for user in data["users"]
        ]

        return tweets, users

    def post_retweet(self, tweet: Tweet):
        logger.info(f"Posting retweet for tweet {tweet}")

        res = self.oauth.post(
            f"https://api.twitter.com/2/users/{self.user.id}/retweets",
            json={"tweet_id": tweet.id},
        )
        res.raise_for_status()

        logger.info(f"Successfully retweeted {tweet}")
