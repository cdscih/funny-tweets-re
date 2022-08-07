# Description

Funny tweets retweet bot.

# Instructions

1. Generate your access token with the account you want to use the bot on
2. Set the environment variables for the script
3. Launch the script

## (1) Generation of access token

The flow used from the script to generate the lifelong access token is called "OAuth 2.0 Authorization Code Flow with PKCE".

The following env variables should be populated:
```bash
USER_ID=
API_KEY=
API_SECRET_KEY=
ACCESS_TOKEN=
ACCESS_TOKEN_SECRET=
```

The `USER_ID` is the unique identifier associated with the bot's account. Find it online through tools like [tweeterid](https://tweeterid.com/).

Both the `API_KEY` and `API_SECRET_KEY` you'll find in the developer twitter portal of your account, the other two through the script `make generate_token`.  
After launching that script, give authorization to the app to use the account and extract the `oauth_verifier` from the params of the url you get redirected to.  

It's not the cleanest method, but it gets the job done. Feel free to suggest improvements or send a pr to make it better!

Note: For more info find the official docs at this [link](https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code).  

# Flow

1. Extract potential retweets
2. re-tweet one
3. save retweeted in list to avoid duplicates (max 1000)


## (1) Extraction

The tweets to potentially use should come from:
* followed accounts (must only be 100% jokes)
* liked tweets
* cdscih's mentions of the bot's account

No extracted tweet should be in the "already tweeted" list.
The extraction should happen once every day.  
The extracted potential tweets should be written in an online free db (like google sheets) and they should be unique.  
Ideally it would work in append mode, so it doesn't do any extra steps.  
Every month the list gets resetted to 0.  

## (2) Retweet

Out of the full list of possible choices, it's just gonna take a random one.  
Perhaps there could be some sort categories, like "followed accs", "randomly liked tweets", "mentions", and tweet once per category..  
After the retweet, it should be added to a retweeted list, written on an online free db. This list should be of fixed size, using a LIFO policy.  
