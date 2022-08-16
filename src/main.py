import os
import sys
import json
import time
import random
import logging
import schedule

from adapters.twitter import Twitter
from adapters.firestore import Firestore
from utils import choose_tweet_to_retweet

logging.basicConfig(
    level=os.environ.get("LOGGER_LEVEL", "INFO"),
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)


logger = logging.getLogger(__name__)

tw = Twitter(
    **{
        "owner_user_id": os.environ.get("OWNER_USER_ID"),
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


def launch():
    try:
        posted_retweets = fs.get_posted_retweets()

        # 1st priority to mentions from owner
        tweets, users = tw.get_tweets_from_owner_mentions()
        tweets = list(filter(lambda t: t.id not in posted_retweets, tweets))

        # 2nd priority to tweets liked
        if len(tweets) == 0:
            tweets, users = tw.get_tweets_from_liked()
            tweets = list(filter(lambda t: t.id not in posted_retweets, tweets))

        # 3rd priority to tweets of followed users
        if len(tweets) == 0:
            users = tw.get_followed_users_list()
            for user in users:
                tweets.extend(tw.get_recent_tweets(user))
            tweets = list(filter(lambda t: t.id not in posted_retweets, tweets))

        if len(tweets) == 0:
            raise ValueError("No retweets candidate found")

        chosen_tweet = choose_tweet_to_retweet(tweets, users)

        tw.post_retweet(chosen_tweet.id)
        fs.save_posted_retweet(chosen_tweet)

    except Exception as err:
        logger.error(err)
        raise err


if __name__ == "__main__":
    launch()
    if len(sys.argv) > 1:
        if "--scheduled" in sys.argv:
            schedule_every_hours = int(os.environ.get("SCHEDULE_EVERY_HOURS", 6))
            logger.info(
                f"Scheduling the job to be run every {schedule_every_hours} hours"
            )
            schedule.every(schedule_every_hours).hours.do(launch)
            while True:
                schedule.run_pending()
                time.sleep(60)
    exit()
