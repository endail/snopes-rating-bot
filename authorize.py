from src.twitter import twitter
from src.store import store

if __name__ == "__main__":

  with twitter.get_oauth_handler() as handler:
    
    print(handler.get_authorization_url())
    url = input("URL: ")

    token = handler.fetch_token(url)
    
    store.set_oauth_token(token)
    print("done")
