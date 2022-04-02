if __name__ == '__main__':

  import sys
  sys.path.insert(0, './src')

  from store import store
  from twitter import twitter
  import tweepy

  token = store.get_oauth_token()
  if twitter.token_has_expired(token):
    token = twitter.get_access_token(token)
    store.set_oauth_token(token)

client = tweepy.Client(bearer_token=token['access_token'])

try:
  client.create_tweet(text='token test 2', user_auth=False)
except Exception as ex:
  print(ex)
