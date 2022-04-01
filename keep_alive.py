from flask import Flask
from threading import Thread
from waitress import serve
from datetime import datetime

app = Flask("snopes-rating-bot")

@app.route("/")
def home():
  return str(datetime.utcnow())

def run():
  serve(app, host="0.0.0.0", port=80, threads=2)
  #app.run(host="0.0.0.0", port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
