import celery.states as states

from decouple import config
from flask import Flask, jsonify, request, url_for
from flask_cors import CORS

from api.services.celery import make_celery
from api.services.validation.file import FileSelectValidator, FileListValidator, FilePathValidator

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default = 'redis://redis:6379/0'),
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default = 'redis://redis:6379/0')
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

    return jsonify(data)

import time
@celery.task(name=f'{app.import_name}.add')
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y

@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task(f'{app.import_name}.add', args=[param1, param2], kwargs={})
    return jsonify({
        'url': f"{url_for('check_task', task_id = task.id, external=True)}",
        'task_id': task.id
    })

@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)

if __name__ == '__main__':
    app.run(host = config('FLASK_HOST', default = '0.0.0.0'), port = config('FLASK_PORT', default = '5000'))
