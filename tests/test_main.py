import pytest

from entities import Tweet


# TODO: fix in ci.. 🙈
@pytest.mark.skip
def test_owner_mentions(mocker, application_tweet_example: Tweet):

    Twitter = mocker.Mock()
    Firestore = mocker.Mock()
    Twitter.return_value = mocker.Mock()
    Firestore.return_value = mocker.Mock()

    tw = Twitter.return_value
    fs = Firestore.return_value

    fs.get_posted_retweets = mocker.Mock(return_value=[])
    tw.get_tweets_from_owner_mentions = mocker.Mock(
        return_value=[application_tweet_example]
    )

    tw.get_tweets_from_liked = mocker.Mock()
    tw.get_followed_users_list = mocker.Mock()

    tw.post_retweet = mocker.Mock()
    fs.save_posted_retweet = mocker.Mock()

    mocker.patch("adapters.twitter.Twitter", new=Twitter)
    mocker.patch("adapters.firestore.Firestore", new=Firestore)

    from main import launch

    launch()

    fs.get_posted_retweets.assert_called_once()
    tw.get_tweets_from_owner_mentions.assert_called_once()
    tw.get_tweets_from_liked.assert_not_called()
    tw.get_followed_users_list.assert_not_called()
    tw.post_retweet.assert_called_once_with(application_tweet_example)
    fs.save_posted_retweet.assert_called_once_with(application_tweet_example)


# TODO: find a way to actually reset mocks for every test 🙈

# from unittest import mock

# def test_liked_tweets(mocker, application_tweet_example: Tweet):

#     Twitter = mocker.Mock()
#     Firestore = mocker.Mock()
#     Twitter.return_value = mocker.Mock()
#     Firestore.return_value = mocker.Mock()

#     tw = Twitter.return_value
#     fs = Firestore.return_value

#     fs.get_posted_retweets = mocker.Mock(return_value=[])
#     tw.get_tweets_from_owner_mentions = mocker.Mock(return_value=[])
#     tw.get_tweets_from_liked = mocker.Mock(return_value=[application_tweet_example])

#     tw.get_followed_users_list = mocker.Mock()

#     tw.post_retweet = mocker.Mock()
#     fs.save_posted_retweet = mocker.Mock()

#     mock.patch.stopall()

#     with mock.patch("adapters.twitter.Twitter", new=Twitter):
#         with mock.patch("adapters.firestore.Firestore", new=Firestore):

#             from main import launch

#             launch()

#             fs.get_posted_retweets.assert_called_once()
#             tw.get_tweets_from_owner_mentions.assert_called_once()
#             tw.get_tweets_from_liked.assert_called_once()
#             tw.get_followed_users_list.assert_not_called()
#             tw.post_retweet.assert_called_once_with(application_tweet_example)
#             fs.save_posted_retweet.assert_called_once_with(application_tweet_example)


# def test_following_users_tweets(
#     mocker, application_tweet_example: Tweet, application_user_example: User
# ):
#     Twitter = mocker.Mock()
#     Firestore = mocker.Mock()
#     Twitter.return_value = mocker.Mock()
#     Firestore.return_value = mocker.Mock()

#     tw = Twitter.return_value
#     fs = Firestore.return_value

#     fs.get_posted_retweets = mocker.Mock(return_value=[])
#     tw.get_tweets_from_owner_mentions = mocker.Mock(return_value=[])
#     tw.get_tweets_from_liked = mocker.Mock(return_value=[])

#     tw.get_followed_users_list = mocker.Mock(return_value=[application_user_example])
#     tw.get_recent_tweets = mocker.Mock(return_value=[application_tweet_example])

#     tw.post_retweet = mocker.Mock()
#     fs.save_posted_retweet = mocker.Mock()

#     mock.patch.stopall()

#     with mock.patch("adapters.twitter.Twitter", new=Twitter):
#         with mock.patch("adapters.firestore.Firestore", new=Firestore):

#             from main import launch

#             launch()

#             fs.get_posted_retweets.assert_called_once()
#             tw.get_tweets_from_owner_mentions.assert_called_once()
#             tw.get_tweets_from_liked.assert_called_once()
#             tw.get_followed_users_list.assert_called_once()
#             tw.get_recent_tweets.assert_called_once_with(application_user_example)
#             tw.post_retweet.assert_called_once_with(application_tweet_example)
#             fs.save_posted_retweet.assert_called_once_with(application_tweet_example)
