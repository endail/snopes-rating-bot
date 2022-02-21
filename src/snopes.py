import html
import json
import os
import urllib
import urllib.request
import urllib.response
from urllib.error import URLError
from htmldom import htmldom

class article:

  def __init__(self):
    self.claim = None
    self.subtitle = None
    self.rating = None
    self.url = None

  def hasRating(self) -> bool:
    return bool(self.rating)

  @classmethod
  def fromdom(cls, node: htmldom.HtmlDomNode):
    art = cls()
    art.claim = html.unescape(node.find("div.media-body > span.title").first().text().strip())
    art.subtitle = html.unescape(node.find("div.media-body > span.subtitle").first().text().strip())
    art.rating = html.unescape(node.find("div.media-body > ul span").text().strip())
    art.url = html.unescape(node.children("a").first().attr("href").strip())
    return art

  @classmethod
  def fromdetail(cls, resp: urllib.response):

    if not resp.url.startswith("https://www.snopes.com/fact-check/"):
      raise URLError("URL does not lead to snopes.com")

    art = cls()

    page = htmldom.HtmlDom().createDom(resp.read().decode("utf-8"))
    art.claim = html.unescape(page.find("div.claim-text").first().text().strip())
    art.subtitle = html.unescape(page.find("main > article > header > h2.subtitle").text().strip())
    art.rating = html.unescape(page.find("div[data-component=claim-rating] span").first().text().strip().lower())
    art.url = resp.url.strip()

    return art


class snopes:

  @staticmethod
  def get_details(url: str) -> article:

    tm = int(os.getenv("APP_SNOPES_DETAIL_TIMEOUT", 10))

    try:
      with urllib.request.urlopen(url, timeout=tm) as resp:
        return article.fromdetail(resp)
    except:
      return None

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

