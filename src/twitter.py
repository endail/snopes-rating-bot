import os
import regex
import time
import tweepy

class twitter:

  @staticmethod
  def get_oauth_handler() -> tweepy.OAuth2UserHandler:
    return tweepy.OAuth2UserHandler(
      client_id=os.getenv('TWITTER_API_CLIENT_ID'),
      redirect_uri=os.getenv('TWITTER_API_REDIRECT_URI'),
      scope=os.getenv('TWITTER_API_SCOPES').split(','),
      client_secret=os.getenv('TWITTER_API_CLIENT_SECRET'))

  @staticmethod
  def get_access_token(token: dict) -> dict:
    handler = __class__.get_oauth_handler()
    return handler.refresh_token(
      os.getenv('TWITTER_API_REFRESH_TOKEN_URI'),
      refresh_token=token['refresh_token'])

  @staticmethod
  def token_has_expired(token: dict) -> bool:
    timeout = int(os.getenv('TWITTER_API_TOKEN_TIMEOUT', 0))
    return (time.time() + timeout) >= token['expires_at']

  @staticmethod
  def get_snopes_tweets(client, mostRecentId: int=None) -> dict:
    return client.search_recent_tweets(
      os.getenv('TWITTER_API_SNOPES_QUERY'),
      since_id=mostRecentId,
      max_results=int(os.getenv('TWITTER_API_SNOPES_MAX_RESULTS')),
      expansions=['attachments.media_keys'],
      tweet_fields=['entities'])

  @staticmethod
  def is_valid_hashtag(tag: str) -> bool:
    # https://stackoverflow.com/a/36902556/570787
    # need to use regex module (not re) for unicode support, spec \p{L}
    pattern = r'(^|\s)([#＃][\w\u05be\u05f3\u05f4]*[\p{L}_]+[\w\u05be\u05f3\u05f4]*)'
    return bool(regex.match(pattern, tag))
