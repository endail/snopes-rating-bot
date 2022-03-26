import os
import tweepy
import time
import logging
import sys
from src.store import store
from src.snopes import snopes, article
from src.twitter import twitter
from keep_alive import keep_alive

def format_tweet(art: article, extInfo: dict) -> str:

  hashtags = [('#' + x) for x in art.getKeywords()]
  hashtags = ' '.join(hashtags)

  # some snopes articles are advertised as interrogatories
  if art.isQuestion():

    symbolPrefix = extInfo['symbol']

    # append a separator
    if symbolPrefix != "":
      symbolPrefix += " "

    return f"{symbolPrefix}{extInfo['display']} #factcheck {hashtags}\n\n{extInfo['short_description']}\n{art.url}"

  else:
    # ...while others are not
    return f"#factcheck {hashtags}\n{art.url}"

def post_tweet(art: article) -> None:

  print("-----")

  if not art.hasRating():
    print(f"Article {art.url} has no rating")
    return

  extInfo = snopes.get_rating_info(art.rating.lower())

  if extInfo == None:
    print(f"Unknown rating {art.rating} for {art.url}")
    return

  reply = format_tweet(art, extInfo)
  print(reply)

  # get stored token
  token = store.get_oauth_token()

  # refresh token if needed
  if twitter.token_has_expired(token):
    print("Token has expired; refreshing now...")
    token = twitter.get_access_token(token)
    store.set_oauth_token(token)

  # setup a tweepy client to post to twitter
  client = tweepy.Client(
    bearer_token=token["access_token"],
    wait_on_rate_limit=True)

  try:

    resp = client.create_tweet(
      text=reply,
      user_auth=False)

    if resp != None and resp.data != None:
      print(f"New tweet link: https://twitter.com/snopesratingbot/status/{resp.data['id']}")

  except tweepy.HTTPException as ex:
    print(ex)
    print(ex.api_codes)
    print(ex.api_messages)
    print(ex.api_errors)

  finally:
    print("-----\n")

def filter_articles(arts: list) -> list:

  arr = []
  last_url = store.get_last_snopes_url()

  # keep adding new articles until the last one has been detected
  for art in arts:
    if art.url == last_url:
      break
    else:
      arr.append(art)

  return arr
  

if __name__ == "__main__":

  # app run guard
  if os.getenv("APP_ENABLED", "False") != "True":
    print("App not enabled; exiting")
    exit()

  # disable logging for replit __logs and __tail
  logging.disable(sys.maxsize)

  # run web server to keep task running
  keep_alive()

  while True:

    try:
      arts = snopes.get_articles()
      print(f"Obtained {len(arts)} articles from snopes.com")

      arts = filter_articles(arts)
      print(f"Filtered down to {len(arts)} articles")

      # tweet in reverse order so most recent article is tweeted last
      for art in reversed(arts):
        post_tweet(art)
        time.sleep(int(os.getenv("APP_TWEET_INTERVAL_TIMEOUT"), 0))

      # store most recent url
      if len(arts) > 0:
        store.set_last_snopes_url(arts[0].url)

    except Exception as ex:
      print(repr(ex))

    # sleep until next check for tweets
    arts.clear()
    print(f"Sleeping for {os.getenv('APP_CHECK_TIMEOUT')} seconds...")
    time.sleep(int(os.getenv("APP_CHECK_TIMEOUT")))
