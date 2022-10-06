from datetime import datetime
import pytz
from flask import Flask
import os

app = Flask(__name__)
SERVER_NAME = os.getenv("SERVER_NAME")
FORMAT = "%d/%m/%Y %H:%M:%S"
TZ = pytz.timezone('Europe/Madrid')

@app.route('/')
def root_path():
    return 'Call to /hello'


@app.route('/hello')
def hello():
    return {'name': SERVER_NAME, 'time': datetime.now(TZ).strftime(FORMAT)}
