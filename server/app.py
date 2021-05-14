import celery.states as states
import pyarrow as pa

from decouple import config
from flask import Flask, jsonify, request, url_for, make_response
from flask_cors import CORS

from api.preprocessing.preprocessor import Preprocessor
from api.processing.processor import Processor
from api.services.cache import Cache
from api.services.celery import make_celery
from api.services.validation.file import FileSelectValidator, FileListValidator, FilePathValidator

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default = 'redis://redis:6379/0'),
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default = 'redis://redis:6379/0'),
    JSON_SORT_KEYS = False
)
CORS(app)
celery = make_celery(app)

cache = Cache()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'name': 'FinView',
        'message': 'Welcome to the FinView app.'
    })

@app.route('/file/select', methods=['POST'])
def file_select():
    validator = FileSelectValidator()
    data = validator.validate(request)
    if data is None: return jsonify(validator.get_error_message()), 400 

    validator = FileListValidator()
    data = validator.validate(data)
    if data is None: return jsonify(validator.get_error_message()), 400 

    validator = FilePathValidator()
    data = validator.validate(data)
    if data is None: return jsonify(validator.get_error_message()), 400 

    task = celery.send_task(f'{app.import_name}.process_file_select', args=[data], kwargs={})
    return jsonify({
        'url': f"{url_for('check_task_progress', task_id = task.id, external=True)}",
        'task_id': task.id
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
    serialised_data = pa.serialize(processed_data).to_buffer().to_pybytes()
    cache.set(f"processed_images_{task_name}", serialised_data, ex = cache_duration)
    return {
        "task": task_name,
        "status": "complete",
        "autodownload": autodownload
    }

@app.route('/file/download/<string:task_name>', methods=['GET'])
def file_download(task_name: str):
    serialised_data = cache.get(f"processed_images_{task_name}")
    if serialised_data is None: return jsonify({"Error": "1", "Message": f"Data not found for task: {task_name}."}), 400 
    deserialised_data = pa.deserialize(serialised_data)
    csv_file = deserialised_data.to_csv(index = False, encoding='utf-8')
    res = make_response(csv_file)
    res.headers["Content-Disposition"] = f"attachment; filename={task_name}.csv"
    res.headers["Content-Type"] = "text/csv"
    return res

@app.route('/check_progress/<string:task_id>', methods=['GET'])
def check_task_progress(task_id: str):
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return jsonify(res.result)

if __name__ == '__main__':
    app.run(host = config('FLASK_HOST', default = '0.0.0.0'), port = config('FLASK_PORT', default = '5000'))
