from entities import Tweet, User


def choose_tweet_to_retweet(tweets: list[Tweet], users: list[User]) -> Tweet:
    users_map = {usr.id: usr.followers_count for usr in users}
    return max(
        tweets,
        key=lambda t: t.like_count / users_map[t.author_id]
        if users_map[t.author_id] != 0
        else 0,
    )
