
[![Heroku Deploy](https://github.com/cdscih/funny-tweets-re/actions/workflows/heroku-deploy.yml/badge.svg)](https://github.com/cdscih/funny-tweets-re/actions/workflows/heroku-deploy.yml)


# Description

Funny tweets retweet bot.  

# Instructions

1. Generate your access token with the account you want to use the bot on
2. Set the environment variables for the script
3. Launch the script

## Generation of the environment variables

The flow used from the script to generate the lifelong access token is called "3-legged OAuth flow". More info [here](https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens)

The following env variables should be populated:
```bash
OWNER_USER_ID=
API_KEY=
API_SECRET_KEY=
ACCESS_TOKEN=
ACCESS_TOKEN_SECRET=
GOOGLE_SERVICE_ACCOUNT=
```

The `OWNER_USER_ID` is the unique identifier associated with the twitter account of the bot's owner. Find it using the script `make get_twitter_user_id` and pasting the owner's twitter username.  
Both the `API_KEY` and `API_SECRET_KEY` you'll find in the developer twitter portal of your account.  
To generate the access tokens, instead, use the script `make generate_token`.  
After launching the script, open the url in the terminal, give authorization to the app to use the account, and extract the `oauth_verifier` from the params of the url you get redirected to.  

It's not the cleanest method, but it gets the job done. Feel free to suggest improvements or send a pr to make it better!

Note: For more info find the official docs at this [link](https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code). 

The `GOOGLE_SERVICE_ACCOUNT` should be the copy-paste of the google service account which has access to the firestore instance used for the bot.

# Flow

1. Extract potential retweets
2. re-tweet one
3. save retweeted in list to avoid duplicates

## (1) Extraction

The retweets candidates will be, in order:
1. [x] owner's mentions of the bot's account
2. [x] liked tweets
3. [x] followed accounts (must only be 100% jokes accounts)

## (2) Retweet

Out of the full list of the retweets candidates, it's going to choose the tweet with the highest relevance based on the rateo of tweet likes to users followers.

### Features to possibly implement
- [ ] Post more than 1 tweet based on categories (eg. Daily, or from the Liked Tweets)
