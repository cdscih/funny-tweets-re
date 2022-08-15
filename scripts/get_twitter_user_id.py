import os
from beeprint import pp
from requests_oauthlib import OAuth1Session


usernames = input(
    "Insert the usernames (tags) of the wanted users separated by a comma:\n"
)

oauth_sessiong = OAuth1Session(
    client_key=os.environ.get("API_KEY"),
    client_secret=os.environ.get("API_SECRET_KEY"),
    resource_owner_key=os.environ.get("ACCESS_TOKEN"),
    resource_owner_secret=os.environ.get("ACCESS_TOKEN_SECRET"),
)

res = oauth_sessiong.get(f"https://api.twitter.com/2/users/by?usernames={usernames}")

twitter_user_ids = [user["id"] for user in res.json()["data"]]

users_dict = {user: twitter_user_ids[i] for i, user in enumerate(usernames.split(","))}

pp(users_dict)
