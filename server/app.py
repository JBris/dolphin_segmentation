import celery.states as states
import json

from decouple import config
from flask import Flask, jsonify, request, url_for
from flask_cors import CORS

from api.preprocessing.preprocessor import Preprocessor
from api.services.celery import make_celery
from api.services.validation.file import FileSelectValidator, FileListValidator, FilePathValidator

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default = 'redis://redis:6379/0'),
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default = 'redis://redis:6379/0'),
    JSON_SORT_KEYS = False
)
celery = make_celery(app)
CORS(app)

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

    return process_file_select(data)
    # task = celery.send_task(f'{app.import_name}.process_file_select', args=[data], kwargs={})
    # return jsonify({
    #     'url': f"{url_for('check_task_progress', task_id = task.id, external=True)}",
    #     'task_id': task.id
    # })


@celery.task(name=f'{app.import_name}.process_file_select')
def process_file_select(data):
    preprocessed_data = Preprocessor().preprocess(data)
    return preprocessed_data

@app.route('/check_progress/<string:task_id>')
def check_task_progress(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return json.dumps(res.result)

if __name__ == '__main__':
    app.run(host = config('FLASK_HOST', default = '0.0.0.0'), port = config('FLASK_PORT', default = '5000'))
