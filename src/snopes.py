import html
from htmldom import htmldom
import json
import os
import spacy
import urllib
import urllib.request
import urllib.response
from urllib.error import URLError
from itertools import takewhile
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
    # remove end quote marks before checking for ?
    # eg. Did Will Smith Make an Alopecia Joke on ‘The Arsenio Hall Show?’
    return self.claim.rstrip('"’\'').endswith('?')

  def getKeywords(self) -> list:

    tokens = []
    # https://machinelearningknowledge.ai/tutorial-on-spacy-part-of-speech-pos-tagging/#Spacy_POS_Tags_List
    pos_tags = ['PROPN', 'NOUN', 'ADJ', 'VERB', 'X']
    nlp = spacy.load(os.getenv('APP_SPACY_MODEL'))
    doc = nlp(self.claim)

    for token in doc:

      # ignore stop characters, punctuation, digits, and whitespace
      if token.is_stop or token.is_punct or token.is_digit or token.is_space:
        continue

      # ignore quote marks, currency symbols, urls, and email addresses
      if token.is_quote or token.is_currency or token.like_url or token.like_email:
        continue

      # ignore non selected parts of speech
      if token.pos_ not in pos_tags:
        continue

    # get a unique list of tokens based on lower case
    # see: https://spacy.io/usage/linguistic-features
    return list(set([token.lemma_ for token in tokens]))

  def getHashtags(self) -> list:
    return list(f"#{k}" for k in self.getKeywords() if twitter.is_valid_hashtag(f"#{k}"))

  @classmethod
  def fromdom(cls, node: htmldom.HtmlDomNode):
    art = cls()
    art.claim = html.unescape(node.find('div.media-body > span.title').first().text().strip())
    art.subtitle = html.unescape(node.find('div.media-body > span.subtitle').first().text().strip())
    art.rating = html.unescape(node.find('div.media-body > ul span').text().strip())
    art.url = html.unescape(node.children('a').first().attr('href').strip())
    return art

  @classmethod
  def fromdetail(cls, resp: urllib.response):

    if not resp.url.startswith(os.getenv('APP_SNOPES_FACT_CHECK_URI')):
      raise URLError(f"URL ({resp.url}) does not lead to {os.getenv('APP_SNOPES_FACT_CHECK_URI')}")

    art = cls()

    page = htmldom.HtmlDom().createDom(resp.read().decode('utf-8'))
    art.claim = html.unescape(page.find('div.claim-text').first().text().strip())
    art.subtitle = html.unescape(page.find('main > article > header > h2.subtitle').text().strip())
    art.rating = html.unescape(page.find('div[data-component=claim-rating] span').first().text().strip().lower())
    art.url = resp.url.strip()

    return art


class snopes:

  @staticmethod
  def get_details(url: str) -> article:

    tm = int(os.getenv('APP_SNOPES_DETAIL_TIMEOUT', 10))

    try:
      with urllib.request.urlopen(url, timeout=tm) as resp:
        return article.fromdetail(resp)
    except:
      return None

  @staticmethod
  def get_articles() -> list:

    arr = []
    url = os.getenv('APP_SNOPES_FACT_CHECK_URI')
    tm = int(os.getenv('APP_SNOPES_FACT_CHECK_TIMEOUT', 10))

    with urllib.request.urlopen(url, timeout=tm) as resp:

      page = htmldom.HtmlDom().createDom(resp.read().decode('utf-8'))
      nodes = page.find('div[data-component=archive-list] article')

      for node in nodes:
        try:
          arr.append(article.fromdom(node))
        except Exception as ex:
          print(repr(ex))
          continue

    return arr

  @staticmethod
  def get_new_articles(lastUrl: str=None) -> list:
    return takewhile(lambda a: a.url != lastUrl, snopes.get_articles())

  @staticmethod
  def get_rating_info(rating: str) -> dict:

    file = os.getenv('APP_SNOPES_RATING_FILE', None)

    try:
      with open(file, 'r', encoding='utf-8') as f:
        for r in json.load(f):
          if r['name'] == rating:
            return r
    except:
      return None
