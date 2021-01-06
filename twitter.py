import tweepy
from keys import api_key, api_secret_key


auth = tweepy.OAuthHandler(api_key, api_secret_key)
# auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.get_user('twitter')

print(user.screen_name)
print(user.followers_count)
for friend in user.friends():
    print(friend.screen_name)