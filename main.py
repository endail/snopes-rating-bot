import os
import tweepy
import time
from src.store import store
from src.snopes import snopes
from src.twitter import twitter
from keep_alive import keep_alive

def post_reply(client: tweepy.Client, snInfo: dict, snTweet: dict) -> None:

  print("-----")

  extInfo = snopes.get_rating_info(snInfo["rating"])

  if extInfo == None:
    print(f"Unknown rating {snInfo['rating']}")
    return

  reply = f"This claim is rated: {extInfo['display']}\n{snInfo['final_url']}"
  print(reply)

  try:

    resp = client.create_tweet(
      text=reply,
      #in_reply_to_tweet_id=snTweet.id,
      reply_settings="following",
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

if __name__ == "__main__":

  # app run guard
  if os.getenv("APP_ENABLED", "False") != "True":
    print("App not enabled; exiting")
    exit()

  # run web server to keep task running
  keep_alive()

  print("Getting details from database")
  mostRecentId = store.get_last_twitter_id()
  token = store.get_oauth_token()

  while True:

    # refresh token if needed
    if twitter.token_has_expired(token):
      print("Token has expired; refreshing now...")
      token = twitter.get_access_token(token)
      store.set_oauth_token(token)

    # setup a tweepy client to query twitter
    client = tweepy.Client(
      bearer_token=token["access_token"],
      wait_on_rate_limit=True)

    # get snopes tweets
    resp = twitter.get_snopes_tweets(client, mostRecentId=mostRecentId)

    if resp != None and resp.meta["result_count"] > 0:

      print(f"Obtained {resp.meta['result_count']} tweets")

      # iterate over tweets in reverse so oldest are handled first
      for tweet in reversed(resp.data):

        # get info from the url in the tweet
        info = snopes.get_details(tweet.entities["urls"][0]["expanded_url"])

        # skip for any which don't return a valid rating
        if info["rating"] == None:
          print(f"Ignoring tweet https://twitter.com/snopes/status/{tweet.id}")
          continue

        post_reply(client, info, tweet)
        time.sleep(int(os.getenv("APP_TWEET_INTERVAL_TIMEOUT"), 0))

      # store most recent id
      mostRecentId = resp.meta["newest_id"]
      store.set_last_twitter_id(resp.meta["newest_id"])

    # sleep until next check for tweets
    print(f"Sleeping for {os.getenv('APP_CHECK_TIMEOUT')} seconds...")
    time.sleep(int(os.getenv("APP_CHECK_TIMEOUT")))
