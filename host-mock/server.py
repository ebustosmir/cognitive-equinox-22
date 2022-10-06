from flask import Flask
import os

app = Flask(__name__)
SERVER_NAME = os.getenv("SERVER_NAME")


@app.route('/')
def hello():
    return '%s' % SERVER_NAME


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)