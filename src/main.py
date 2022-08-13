import os
import logging
import random

from twitter import Twitter

logging.basicConfig(
    level=os.environ.get("LOGGER_LEVEL", "INFO"),
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

tw = Twitter(
    **{
        "user_id": os.environ.get("USER_ID"),
        "consumer_key": os.environ.get("API_KEY"),
        "consumer_secret": os.environ.get("API_SECRET_KEY"),
        "access_token": os.environ.get("ACCESS_TOKEN"),
        "access_token_secret": os.environ.get("ACCESS_TOKEN_SECRET"),
    }
)

try:
    logger.info("Retrieving the list of tweets to possibly retweet..")

    followed_users = tw.get_followed_users_list()

    tweets = []

    for user in followed_users:
        logger.info(f"Retrieving tweets of {user.username}")
        tweets.extend(tw.get_recent_tweets_ids(user.id))

    chosen_tweet = random.choice(tweets)

    logger.info(f"Posting retweet of {chosen_tweet}")
    tw.post_retweet(chosen_tweet)

    logger.info(f"Successfully retweeted {chosen_tweet}")

except Exception as err:
    logger.error(err)
    raise err
