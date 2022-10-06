from flask import Flask
import os

app = Flask(__name__)
SERVER_NAME = os.getenv("SERVER_NAME")


@app.route('/')
def hello():
    return '%s' % SERVER_NAME
