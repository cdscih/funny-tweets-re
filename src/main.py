import sys
import time
import logging
import schedule

from config import CONFIG
from adapters.twitter import Twitter
from adapters.firestore import Firestore
from entities import Tweet
from utils import choose_tweet_to_retweet


logger = logging.getLogger(__name__)


def launch():
    try:
        tw = Twitter(**CONFIG["adapters"]["twitter"])
        fs = Firestore(**CONFIG["adapters"]["firebase"])

        posted_retweets = fs.get_posted_retweets()

        def exclude_already_posted(tweets: list[Tweet]) -> list[Tweet]:
            return list(filter(lambda t: t.id not in posted_retweets, tweets))

        # 1st priority to mentions from owner
        tweets = exclude_already_posted(tw.get_tweets_from_owner_mentions())

        # 2nd priority to tweets liked
        if len(tweets) == 0:
            logger.info("No available tweets found from owner mentions")
            tweets = exclude_already_posted(tw.get_tweets_from_liked())
            tweets = list(filter(lambda t: t.id not in posted_retweets, tweets))

        # 3rd priority to tweets of followed users
        if len(tweets) == 0:
            logger.info("No available liked tweets found")
            users = tw.get_followed_users_list()
            for user in users:
                tweets.extend(tw.get_recent_tweets(user))
            tweets = exclude_already_posted(tweets)

        if len(tweets) == 0:
            raise ValueError("No retweets candidate found")

        chosen_tweet = choose_tweet_to_retweet(tweets)

        tw.post_retweet(chosen_tweet)
        fs.save_posted_retweet(chosen_tweet)

    except Exception as err:
        logger.error(err)
        raise err


if __name__ == "__main__":
    launch()
    if len(sys.argv) > 1:
        if "--scheduled" in sys.argv:
            schedule_every_hours = CONFIG["schedule_every_hours"]
            logger.info(
                f"Scheduling the job to be run every {schedule_every_hours} hours"
            )
            schedule.every(schedule_every_hours).hours.do(launch)
            while True:
                schedule.run_pending()
                time.sleep(60)
    exit()
