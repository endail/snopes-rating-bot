import logging
import os
import sys
import tweepy
import time
from src.keep_alive import keep_alive
from src.util import dotsleep
from src.store import store
from src.snopes import snopes, article
from src.twitter import twitter

def format_tweet(art: article, extInfo: dict) -> str:

  hashtags = art.getHashtags()
  hashtagStr = os.getenv('APP_DEFAULT_HASHTAGS', '')

  if len(hashtags) > 0:
    hashtagStr += f" {' '.join(art.getHashtags())}"

  # some snopes articles are advertised as interrogatories (ie. ending in a "?")
  if art.isQuestion():
    symbolPrefix = (extInfo['symbol'] + ' ') if extInfo['symbol'] != None else ''
    return f"{symbolPrefix}{extInfo['display']}\n{hashtagStr}\n{art.url}"
  else:
    return f"{hashtagStr}\n{art.url}"

def post_tweet(art: article) -> None:

  print('-----')

  if not art.hasRating():
    print(f"Article {art.url} has no rating")
    return

  extInfo = snopes.get_rating_info(art.rating.lower())

  if extInfo == None:
    print(f"Unknown rating {art.rating} for {art.url}")
    return

  reply = format_tweet(art, extInfo)
  print(reply)

  # refresh token if needed
  token = store.get_oauth_token()
  if twitter.token_has_expired(token):
    print('Token has expired; refreshing now...')
    token = twitter.get_access_token(token)
    store.set_oauth_token(token)

  # setup a tweepy client to post to twitter
  client = tweepy.Client(
    bearer_token=token['access_token'],
    wait_on_rate_limit=True)

  try:
    resp = client.create_tweet(
      text=reply,
      user_auth=False)

    if resp != None and resp.data != None:
      print(f"New tweet link: {twitter.get_tweet_link(resp.data['id'], os.getenv('APP_TWITTER_BOT_USERNAME'))}")

  except tweepy.HTTPException as ex:
    print(ex)
    print(ex.api_codes)
    print(ex.api_messages)
    print(ex.api_errors)

  finally:
    print(f"-----{os.linesep}")


if __name__ == '__main__':

  # disable logging for replit __logs and __tail
  logging.disable(sys.maxsize)

  # app run guard
  if os.getenv('APP_ENABLED', 'False') != 'True':
    print('App not enabled; exiting')
    exit()

  # run web server to keep task running
  keep_alive()

  # list of articles, periodically cleared after each check
  arts = []
  newArts = []
  exUrls = []

  while True:

    try:

      #1. get list of existing urls
      exUrls = store.get_last_snopes_articles()

      #2. get the new articles
      newArts = snopes.get_articles()

      #3. filter
      arts = filter(lambda a: a.url not in exUrls, newArts)

      print(f"Obtained {len(arts)} new articles from snopes.com")

      # tweet in reverse order so most recent article is tweeted last
      for art in reversed(arts):
      #  post_tweet(art)
        time.sleep(int(os.getenv('APP_TWEET_INTERVAL_TIMEOUT', 0)))
      
      store.set_last_snopes_articles([a.url for a in newArts])

    except Exception as ex:
      print(repr(ex))

    # sleep until next check for tweets
    arts.clear()
    print(f"Sleeping for {os.getenv('APP_CHECK_TIMEOUT')} seconds...")
    dotsleep(int(os.getenv('APP_CHECK_TIMEOUT')))
