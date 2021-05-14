
from decouple import config
from flask import Flask, jsonify, current_app
from flask_cors import CORS

from api.preprocessing.preprocessor import Preprocessor
from api.processing.processor import Processor
from api.routes.file  import file_api
from api.services.cache import Cache
from api.services.celery import make_celery
from api.services.serializer import Serializer

app = Flask(__name__)
CORS(app)
app.config.update(
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default = 'redis://redis:6379/0'),
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default = 'redis://redis:6379/0'),
    JSON_SORT_KEYS = False,
)

celery = make_celery(app)
app.config["FILE_WORKER"] = celery
app.config["CACHE"] = Cache()

app.register_blueprint(file_api)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'name': 'FinView',
        'message': 'Welcome to the FinView app.'
    })

@celery.task(name=f'{app.import_name}.process_file_select')
def process_file_select(data):
    task_name = data["name"]

    if isinstance(data.get("cache_duration"), int): cache_duration = data["cache_duration"]
    else: cache_duration = config('CACHE_DURATION', default = 86400, cast = int)

    if data.get("autodownload") == 1 or data.get("autodownload") == 0: autodownload = data["autodownload"]
    else: autodownload = config('AUTODOWNLOAD_FILE', default = 1, cast = int)

    preprocessed_data = Preprocessor().preprocess(data)
    processed_data = Processor().process(preprocessed_data)
    serialised_data = Serializer().serialize(processed_data) 
    current_app.config["CACHE"].set(f"processed_images_{task_name}", serialised_data, ex = cache_duration)
    return {
        "task": task_name,
        "status": "complete",
        "autodownload": autodownload
    }

if __name__ == '__main__':
    app.run(host = config('FLASK_HOST', default = '0.0.0.0'), port = config('FLASK_PORT', default = '5000'))
