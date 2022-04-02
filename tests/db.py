if __name__ == '__main__':

  import sys
  sys.path.insert(0, './src')
  from store import store

  print(store.get_oauth_token())
  print(store.get_last_twitter_id())