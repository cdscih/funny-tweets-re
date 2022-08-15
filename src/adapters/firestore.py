import os
import pendulum
import logging
import firebase_admin

from firebase_admin import credentials, firestore

from entities import Tweet

logger = logging.getLogger(__name__)


class Firestore:

    POSTED_RETWEETS_COLLECTION = "posted_retweets"

    def __init__(self, service_account: str):
        cred = credentials.Certificate(service_account)
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()
        self._cleanup()

    def _cleanup(self):
        logger.info(f"Cleaning up {self.POSTED_RETWEETS_COLLECTION} collection")
        for doc in self.client.collection(self.POSTED_RETWEETS_COLLECTION).get():
            if doc.create_time < pendulum.now().subtract(
                months=int(os.environ.get("EXPIRE_AFTER_MONTHS", 1))
            ):
                self.client.collection(self.POSTED_RETWEETS_COLLECTION).document(
                    doc.id
                ).delete()

    def save_posted_retweet(self, tweet: Tweet):
        logger.info("Storing posted retweet")
        self.client.collection(self.POSTED_RETWEETS_COLLECTION).document(tweet.id).set(
            {
                "tweet_id": tweet.id,
                "author_id": tweet.author_id,
                "like_count": tweet.like_count,
            }
        )

    def get_posted_retweets(self):
        logger.info("Retrieving posted retweets")
        return {
            doc.id
            for doc in self.client.collection(self.POSTED_RETWEETS_COLLECTION).get()
        }
