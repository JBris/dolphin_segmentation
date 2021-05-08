import os

from decouple import config
from flask import Flask, jsonify
from flask_cors import CORS

from api.services.cache import Cache

app = Flask(__name__)
CORS(app)

cache = Cache()

def get_hit_count():
    retries = 5
    return cache.incr('hits')

@app.route('/')
def home():
    return jsonify({'views': get_hit_count()})

if __name__ == '__main__':
    app.run(host = config('FLASK_HOST', default = '0.0.0.0'), port = config('FLASK_PORT', default = '5000'))
