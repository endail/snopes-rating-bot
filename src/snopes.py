import json
import os
import urllib
from htmldom import htmldom
from urllib.error import URLError

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
  def get_articles() -> dict:

    snFCUrl = "https://www.snopes.com/fact-check/"

    with urllib.request.urlopen(snFCUrl) as resp:

      page = htmldom.HtmlDom().createDom(resp.read().decode("utf-8"))
      body > div.container.mt-3 > div > div.col-12.col-lg-8.mb-3 > main > div.card.list-archive > div



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
