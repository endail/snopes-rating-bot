from src.store import store

if __name__ == "__main__":

  defaultToken = {
    "access_token": "",
    "refresh_token": "",
    "expires_at": 0
  }

  store.set_oauth_token(defaultToken)
  store.set_last_twitter_id(None)
  print("done")
