import html
import json
import os
import urllib
import urllib.request
from urllib.error import URLError
from htmldom import htmldom

class snopes:

  @staticmethod
  def get_details(url: str) -> dict:
  
    info = {
      "final_url": None,
      "claim": None,
      "rating": None
    }

    tm = int(os.getenv("APP_SNOPES_DETAIL_TIMEOUT", 10))

    try:
      with urllib.request.urlopen(url, timeout=tm) as resp:
        
        info["final_url"] = resp.url

        if not resp.url.startswith("https://www.snopes.com"):
          raise URLError("url does not lead to snopes.com")

        page = htmldom.HtmlDom().createDom(resp.read().decode("utf-8"))
        info["claim"] = page.find("div.claim-text").first().text().strip()
        info["rating"] = page.find("div[data-component=claim-rating] span").first().text().strip().lower()

    except:
      pass

    return info

  @staticmethod
  def get_articles() -> list:

    arr = []
    url = os.getenv("APP_SNOPES_FACT_CHECK_URI")
    tm = int(os.getenv("APP_SNOPES_FACT_CHECK_TIMEOUT", 10))

    with urllib.request.urlopen(url, timeout=tm) as resp:

      page = htmldom.HtmlDom().createDom(resp.read().decode("utf-8"))
      nodes = page.find("div[data-component=archive-list] article")

      for node in nodes:
        try:
          arr.append(article.fromdom(node))
        except Exception as ex:
          print(repr(ex))
          continue

    return arr

  @staticmethod
  def get_rating_info(rating: str) -> dict:

    file = os.getenv("APP_SNOPES_RATING_FILE", None)

    try:
      with open(file, "r", encoding="utf-8") as f:
        for r in json.load(f):
          if r["name"] == rating:
            return r
    except:
      return None


class article:

  def __init__(self):
    self.title = None
    self.subtitle = None
    self.rating = None
    self.url = None

  def hasRating(self) -> bool:
    return bool(self.rating)

  @classmethod
  def fromdom(cls, node: htmldom.HtmlDomNode):
    art = cls()
    art.title = html.unescape(node.find("div.media-body > span.title").first().text().strip())
    art.subtitle = html.unescape(node.find("div.media-body > span.subtitle").first().text().strip())
    art.rating = html.unescape(node.find("div.media-body > ul span").text().strip())
    art.url = html.unescape(node.children("a").first().attr("href"))
    return art
