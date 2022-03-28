import html
import json
import os
import urllib
import urllib.request
import urllib.response
from urllib.error import URLError
from htmldom import htmldom
import spacy
from .twitter import twitter

class article:

  def __init__(self):
    self.claim = None
    self.subtitle = None
    self.rating = None
    self.url = None

  def hasRating(self) -> bool:
    return bool(self.rating)

  def isQuestion(self) -> bool:
    return self.claim.endswith("?")

  def getKeywords(self) -> list:

    tokens = []
    pos_tags = ["PROPN", "NOUN"]
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(self.claim)

    for token in doc:

      # ignore stop characters, punctuation, digits, and whitespace
      if token.is_stop or token.is_punct or token.is_digit or token.is_space:
        continue

      # ignore quote marks, currency symbols, urls, and email addresses
      if token.is_quote or token.is_currency or token.like_url or token.like_email:
        continue

      if token.pos_ not in pos_tags:
        continue

      # check if the token would be a valid twitter hashtag
      if twitter.is_valid_hashtag("#" + token.text):
        tokens.append(token)

    # get a unique list of tokens based on lower case
    return list(set(["#" + token.lemma_.lower() for token in tokens]))

    #nlp = spacy.load("en_core_web_sm")
    #result = []
    #pos_tag = ['PROPN', 'NOUN']
    #doc = nlp(self.claim.lower())

    #for token in doc:
    #  
    #  if token.text in nlp.Defaults.stop_words or token.text in punctuation:
    #    continue

    #  if token.pos_ in pos_tag:
    #    result.append(token.text)

    #return set(result)

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

