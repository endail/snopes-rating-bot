from src.store import store

if __name__ == '__main__':

  defaultToken = {
    'access_token': 'abc',
    'refresh_token': 'def',
    'expires_at': 0
  }

  store.set_oauth_token(defaultToken)
  store.set_last_twitter_id(None)
  store.set_last_snopes_url(None)
  store.set_last_snopes_articles([])
  print('done')
