import pytest
import pendulum

from types import SimpleNamespace
from adapters.firestore import Firestore
from entities import Tweet


@pytest.fixture
def fs(mocker, fs_config):
    mocker.patch("firebase_admin.credentials.Certificate", autospec=True)
    mocker.patch("firebase_admin.initialize_app", autospec=True)
    mocker.patch("firebase_admin.firestore.client", autospec=True)

    yield Firestore(**fs_config)

    mocker.resetall()


def test__cleanup(fs: Firestore, mocker, fs_config):

    document_id = "document_id"

    fs.client.collection = mocker.Mock()
    fs.client.collection.return_value.get = mocker.Mock(
        return_value=[
            SimpleNamespace(
                id=document_id,
                create_time=pendulum.now().subtract(
                    days=(fs_config["collection_expire_after_days"] + 1)
                ),
            )
        ]
    )
    fs.client.collection.return_value.document = mocker.Mock()
    fs.client.collection.return_value.document.return_value.delete = mocker.Mock()

    fs._cleanup()

    assert fs.client.collection.call_count == 2

    for call in fs.client.collection.call_args_list:
        assert call[0][0] == fs.POSTED_RETWEETS_COLLECTION.name

    fs.client.collection.return_value.get.assert_called_once()
    fs.client.collection.return_value.document.assert_called_once_with(document_id)
    fs.client.collection.return_value.document.return_value.delete.assert_called_once()


def test_save_posted_retweet(fs: Firestore, mocker, application_tweet_example: Tweet):

    fs.client.collection = mocker.Mock()
    fs._cleanup = mocker.Mock()
    fs.client.collection.return_value.document = mocker.Mock()
    fs.client.collection.return_value.document.return_value.set = mocker.Mock()

    fs.save_posted_retweet(application_tweet_example)

    fs._cleanup.assert_called_once()
    fs.client.collection.assert_called_once_with(fs.POSTED_RETWEETS_COLLECTION.name)
    fs.client.collection.return_value.document.assert_called_once_with(
        application_tweet_example.id
    )
    fs.client.collection.return_value.document.return_value.set.assert_called_once_with(
        application_tweet_example.dict()
    )


def test_get_posted_retweets(fs: Firestore, mocker, application_tweet_example: Tweet):

    fs.client.collection = mocker.Mock()
    fs.client.collection.return_value.get = mocker.Mock(
        return_value=[
            SimpleNamespace(id=application_tweet_example.id),
            SimpleNamespace(id=application_tweet_example.id),
        ]
    )

    res = fs.get_posted_retweets()

    fs.client.collection.assert_called_once_with(fs.POSTED_RETWEETS_COLLECTION.name)
    fs.client.collection.return_value.get.assert_called_once()

    assert len(res) == 1
