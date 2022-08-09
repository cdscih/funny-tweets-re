import os
import logging

from twitter import Twitter

logging.basicConfig(
    level=os.environ.get("LOGGER_LEVEL", "INFO"),
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

twitter_config = {
    "user_id": os.environ.get("USER_ID"),
    "consumer_key": os.environ.get("API_KEY"),
    "consumer_secret": os.environ.get("API_SECRET_KEY"),
    "access_token": os.environ.get("ACCESS_TOKEN"),
    "access_token_secret": os.environ.get("ACCESS_TOKEN_SECRET"),
}

tw = Twitter(**twitter_config)

tw.post_retweet("1556671336453476355")
