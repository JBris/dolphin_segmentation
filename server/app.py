import os

from flask import Flask, jsonify

from api.services.cache import Cache

app = Flask(__name__)
cache = Cache()

def get_hit_count():
    retries = 5
    return cache.incr('hits')

@app.route('/')
def home():
    return jsonify({'views': get_hit_count()})

if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_HOST', '0.0.0.0'), port=os.getenv('FLASK_PORT', '5000'))
