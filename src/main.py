import os
import logging
import random
import json

from twitter import Twitter
from firestore import Firestore

from utils import choose_tweet_to_retweet

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

fs = Firestore(
    **{
        "service_account": json.loads(
            os.environ.get("GOOGLE_SERVICE_ACCOUNT"),
            strict=False,
        )
    }
)

try:
    followed_users = tw.get_followed_users_list()
    tweets = []
    for user in followed_users:
        tweets.extend(tw.get_recent_tweets_ids(user))
    if len(tweets) == 0:
        raise ValueError("No retweets candidate found")
    chosen_tweet = choose_tweet_to_retweet(tweets, followed_users)
    tw.post_retweet(chosen_tweet.id)
    fs.save_posted_retweet(chosen_tweet)
except Exception as err:
    logger.error(err)
    raise err
