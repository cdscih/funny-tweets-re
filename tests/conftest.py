import pytest

from adapters.twitter import build_tweets, build_user


@pytest.fixture
def twitter_user_example():
    return {
        "id": "user_id",
        "name": "name",
        "username": "username",
        "public_metrics": {"followers_count": 3},
    }


@pytest.fixture
def twitter_tweet_example():
    return {
        "id": "tweet_id",
        "author_id": "user_id",
        "public_metrics": {"like_count": 3},
    }


@pytest.fixture
def application_user_example(twitter_user_example):
    return build_user(twitter_user_example)


@pytest.fixture
def application_tweet_example(twitter_tweet_example, twitter_user_example):
    return build_tweets([twitter_tweet_example], [twitter_user_example])[0]


@pytest.fixture
def tw_config():
    return {
        "owner_user_id": "owner_user_id",
        "consumer_key": "consumer_key",
        "consumer_secret": "consumer_secret",
        "access_token": "access_token",
        "access_token_secret": "access_token_secret",
    }


@pytest.fixture
def fs_config():
    return {
        "service_account": {},
        "collection_expire_after_days": 7,
    }
