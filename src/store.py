from replit import db
import json
import os

class store:

  @staticmethod
  def get_oauth_token() -> dict:
    return json.loads(db.get_raw("oauth_token"))

  @staticmethod
  def set_oauth_token(token: dict) -> None:
    db.set_raw("oauth_token", json.dumps(token))

  @staticmethod
  def get_last_twitter_id() -> str:
    return db["last_twitter_id"]

  @staticmethod
  def set_last_twitter_id(lastId: str) -> None:
    db["last_twitter_id"] = lastId

  @staticmethod
  def get_last_snopes_url() -> str:
    return db["last_snopes_url"]

  @staticmethod
  def set_last_snopes_url(url: str) -> None:
    db["last_snopes_url"] = url
