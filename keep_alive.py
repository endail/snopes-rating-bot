from datetime import datetime
from flask import Flask
import os
from threading import Thread
from waitress import serve

app = Flask(os.getenv('APP_NAME', ''))

@app.route('/')
def home():
  return str(datetime.utcnow())

def run():
  serve(app, host='0.0.0.0', port=80, threads=2)
  #app.run(host="0.0.0.0", port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
