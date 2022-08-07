import httpx
import os


user_id="1480156703412920327"

headers={
    "Authorization": f"Bearer {os.environ.get('BEARER_TOKEN')}"
}

print(os.environ.get('BEARER_TOKEN'))

res = httpx.get(f"https://api.twitter.com/2/users/{user_id}/liked_tweets", headers=headers)

print(res.json())