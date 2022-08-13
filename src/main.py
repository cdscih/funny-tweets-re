import os
import logging
import random

from twitter import Twitter
from firestore import Firestore

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

fs = Firestore()

try:
    followed_users = tw.get_followed_users_list()
    new_retweets_candidates = []
    for user in followed_users:
        new_retweets_candidates.extend(tw.get_recent_tweets_ids(user))
    fs.save_new_retweets_candidates(new_retweets_candidates)
    tweets = fs.get_retweets_candidates()
    if len(tweets) == 0:
        raise ValueError("No retweets candidate found")
    chosen_tweet = random.choice(tweets)
    tw.post_retweet(chosen_tweet.id)
    fs.save_posted_retweet(chosen_tweet)
except Exception as err:
    logger.error(err)
    raise err
