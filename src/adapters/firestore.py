import pendulum
import logging
import firebase_admin
import firebase_admin.firestore as firestore

from types import SimpleNamespace

from entities import Tweet

logger = logging.getLogger(__name__)


class Firestore:
    POSTED_RETWEETS_COLLECTION = SimpleNamespace(
        name="posted_retweets",
        expiration=7,
    )

    def __init__(self, service_account: str, collection_expire_after_days: int):
        self.POSTED_RETWEETS_COLLECTION.expiration = collection_expire_after_days
        cred = firebase_admin.credentials.Certificate(service_account)
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()

    def _cleanup(self):
        collection, exp_days = (
            self.POSTED_RETWEETS_COLLECTION.name,
            self.POSTED_RETWEETS_COLLECTION.expiration,
        )
        logger.info(
            f"Cleaning up {collection} collection removing older than {exp_days} days"
        )
        for doc in self.client.collection(collection).get():
            if doc.create_time < pendulum.now().subtract(days=exp_days):
                self.client.collection(collection).document(doc.id).delete()

    def save_posted_retweet(self, tweet: Tweet):
        self._cleanup()
        collection = self.POSTED_RETWEETS_COLLECTION.name
        logger.info(f"Storing posted retweet in collection {collection}")
        self.client.collection(collection).document(tweet.id).set(tweet.dict())

    def get_posted_retweets(self):
        collection = self.POSTED_RETWEETS_COLLECTION.name
        logger.info(f"Retrieving tweets from collection {collection}")
        return {doc.id for doc in self.client.collection(collection).get()}
