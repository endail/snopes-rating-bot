if __name__ == "__main__":

  import sys
  sys.path.insert(0, './src')
  from store import store

  store.set_last_twitter_id("1492326600221863937")
  print(store.get_oauth_token())
  print(store.get_last_twitter_id())