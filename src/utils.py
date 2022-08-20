from entities import Tweet


def choose_tweet_to_retweet(tweets: list[Tweet]) -> Tweet:
    return max(
        tweets,
        key=lambda t: t.like_count / t.author.followers_count
        if t.author.followers_count != 0
        else 0,
    )
