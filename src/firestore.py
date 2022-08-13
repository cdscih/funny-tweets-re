import os
import pendulum
import logging
import firebase_admin

from firebase_admin import credentials, firestore

from entities import Tweet

logger = logging.getLogger(__name__)


class Firestore:

    POSTED_RETWEETS_COLLECTION = "posted_retweets"
    TWEETS_CANDIDATES_COLLECTION = "tweets_candidates"
    posted_retweets = []

    def __init__(self):
        # TODO: use secret manager from gcp
        cred = credentials.Certificate("service_account.json")
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()
        self._cleanup()
        self.get_posted_retweets()

    def __delete_old(self, collection: str):
        for doc in self.client.collection(collection).get():
            if doc.create_time < pendulum.now().subtract(
                months=int(os.environ.get("EXPIRE_AFTER_MONTHS", 12))
            ):
                self.client.collection(collection).document(doc.id).delete()

    def _cleanup(self):
        collections = [
            self.POSTED_RETWEETS_COLLECTION,
            self.TWEETS_CANDIDATES_COLLECTION,
        ]
        logger.info(f"Cleaning up collections: {collections}")
        for collection in collections:
            self.__delete_old(collection)

    def save_new_retweets_candidates(self, tweets: list[Tweet]):
        retweets_candidates = list(
            filter(lambda tweet: tweet.id not in self.posted_retweets, tweets)
        )
        logger.info(f"Saving {len(retweets_candidates)} retweets candidates")
        for tweet in retweets_candidates:
            self.client.collection(self.TWEETS_CANDIDATES_COLLECTION).document(
                tweet.id
            ).set({"author_id": tweet.author_id})

    def get_retweets_candidates(self) -> list[Tweet]:
        logger.info("Retrieving retweets candidates")
        return [
            Tweet(id=doc.id, author_id=doc.get("author_id"))
            for doc in self.client.collection(self.TWEETS_CANDIDATES_COLLECTION).get()
        ]

    def delete_tweet_from_candidates(self, tweet: Tweet):
        logger.info("Deleting posted retweet from tweets candidates")
        self.client.collection(self.TWEETS_CANDIDATES_COLLECTION).document(
            tweet.id
        ).delete()

    def save_posted_retweet(self, tweet: Tweet):
        logger.info("Storing posted retweet")
        self.client.collection(self.POSTED_RETWEETS_COLLECTION).document(tweet.id).set(
            {"author_id": tweet.author_id}
        )
        self.delete_tweet_from_candidates(tweet)

    def get_posted_retweets(self):
        logger.info("Retrieving posted retweets")
        self.posted_retweets = {
            doc.id
            for doc in self.client.collection(self.POSTED_RETWEETS_COLLECTION).get()
        }
        return self.posted_retweets
