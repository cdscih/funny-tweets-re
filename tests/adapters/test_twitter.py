import pytest

from adapters.twitter import Twitter
from entities import Tweet, User


@pytest.fixture
def tw(requests_mock, twitter_user_example, tw_config):

    data = {"data": twitter_user_example}

    requests_mock.get("https://api.twitter.com/2/users/me", json=data)
    tw = Twitter(**tw_config)
    requests_mock.reset()
    return tw


def test__get_bot_user(tw: Twitter, requests_mock, twitter_user_example):

    url = "https://api.twitter.com/2/users/me"
    requests_mock.get(url, json={"data": twitter_user_example})

    tw._get_bot_user()

    assert len(requests_mock.request_history) == 1
    assert requests_mock.request_history[0].url == f"{url}?user.fields=public_metrics"


def test_get_followed_users_list(tw: Twitter, requests_mock, twitter_user_example):
    url = f"https://api.twitter.com/2/users/{tw.user.id}/following"
    requests_mock.get(
        url,
        json={"data": [twitter_user_example]},
    )

    tw.get_followed_users_list()
    assert len(requests_mock.request_history) == 1
    assert requests_mock.request_history[0].url == f"{url}?user.fields=public_metrics"


def test_get_recent_tweets(
    tw: Twitter,
    requests_mock,
    twitter_user_example,
    twitter_tweet_example,
    application_user_example: User,
):
    url = f"https://api.twitter.com/2/users/{tw.user.id}/tweets"
    requests_mock.get(
        url,
        json={
            "data": [twitter_tweet_example],
            "includes": {"users": [twitter_user_example]},
        },
    )

    tw.get_recent_tweets(application_user_example)
    assert len(requests_mock.request_history) == 1
    assert (
        requests_mock.request_history[0].url
        == f"{url}?expansions=author_id&tweet.fields=public_metrics"
    )


def test_get_tweets_from_liked(
    tw: Twitter, requests_mock, twitter_user_example, twitter_tweet_example
):
    url = f"https://api.twitter.com/2/users/{tw.user.id}/liked_tweets"
    requests_mock.get(
        url,
        json={
            "data": [twitter_tweet_example],
            "includes": {"users": [twitter_user_example]},
        },
    )

    tw.get_tweets_from_liked()
    assert len(requests_mock.request_history) == 1
    assert (
        requests_mock.request_history[0].url
        == f"{url}?expansions=author_id&tweet.fields=author_id%2Cpublic_metrics&user.fields=public_metrics"
    )


def test_get_tweets_from_owner_mentions(
    tw: Twitter, requests_mock, twitter_user_example, twitter_tweet_example, tw_config
):

    url = "https://api.twitter.com/2/tweets/search/recent"
    requests_mock.get(
        url,
        json={
            "includes": {
                "users": [twitter_user_example],
                "tweets": [twitter_tweet_example],
            },
        },
    )

    tw.get_tweets_from_owner_mentions()
    assert len(requests_mock.request_history) == 1
    assert (
        requests_mock.request_history[0].url
        == f"{url}?query=from%3A{tw_config['owner_user_id']}+%40{tw.user.username}+is%3Areply&tweet.fields=author_id%2Cpublic_metrics&user.fields=public_metrics&expansions=referenced_tweets.id%2Creferenced_tweets.id.author_id"  # noqa: E501
    )


def test_post_retweet(tw: Twitter, requests_mock, application_tweet_example: Tweet):

    url = f"https://api.twitter.com/2/users/{tw.user.id}/retweets"
    requests_mock.post(url)

    tw.post_retweet(application_tweet_example)
    assert len(requests_mock.request_history) == 1
    assert requests_mock.request_history[0].url == url
    assert requests_mock.request_history[0].json() == {
        "tweet_id": application_tweet_example.id
    }
