from requests_oauthlib import OAuth1Session


def get_twitter_user_ids_from_usernames(
    oauth_sessiong: OAuth1Session, usernames: str
) -> list[str]:
    res = oauth_sessiong.get(
        f'https://api.twitter.com/2/users/by?usernames={",".join(usernames)}'
    )
    if res.status_code != 200:
        raise Exception(f"Request returned an error: {res.status_code} {res.text}")
    return [user["id"] for user in res.json()["data"]]
