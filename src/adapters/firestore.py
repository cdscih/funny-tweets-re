import os
import pendulum
import logging
import firebase_admin

from firebase_admin import credentials, firestore

from entities import Tweet

logger = logging.getLogger(__name__)


POSTED_RETWEETS_COLLECTION = (
    "posted_retweets",
    int(os.environ.get("EXPIRE_AFTER_DAYS", 7)),
)
RECURRING_POSTED_RETWEETS_COLLECTION = (
    "recurring_posted_retweets",
    int(os.environ.get("RECURRING_EXPIRE_AFTER_DAYS", 365)),
)

COLLECTIONS = [POSTED_RETWEETS_COLLECTION, RECURRING_POSTED_RETWEETS_COLLECTION]


class Firestore:
    def __init__(self, service_account: str):
        cred = credentials.Certificate(service_account)
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()
        self._cleanup()

    def _cleanup(self):
        for coll, exp_days in COLLECTIONS:
            logger.info(
                f"Cleaning up {coll} collection removing older than {exp_days} days"
            )
            for doc in self.client.collection(coll).get():
                if doc.create_time < pendulum.now().subtract(days=exp_days):
                    self.client.collection(coll).document(doc.id).delete()

    def save_posted_retweet(self, tweet: Tweet, recurring=False):
        collection = (
            POSTED_RETWEETS_COLLECTION[0]
            if not recurring
            else RECURRING_POSTED_RETWEETS_COLLECTION[0]
        )
        logger.info(f"Storing posted retweet in collection {collection}")
        self.client.collection(collection).document(tweet.id).set(tweet.dict())

    def get_posted_retweets(self, recurring=False):
        collection = (
            POSTED_RETWEETS_COLLECTION[0]
            if not recurring
            else RECURRING_POSTED_RETWEETS_COLLECTION[0]
        )
        logger.info(f"Retrieving tweets from collection {collection}")
        return {doc.id for doc in self.client.collection(collection).get()}
