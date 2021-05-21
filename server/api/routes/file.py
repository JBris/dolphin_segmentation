import celery.states as states
import os

from flask import Blueprint, json, request, jsonify, current_app, url_for, make_response, send_file

file_api = Blueprint('file', __name__, url_prefix = "/file")

from api.services.content_type import ContentType
from api.services.archiver import Archiver
from api.services.copy import Copy
from api.services.dataset import Dataset
from api.services.deletion import Deletion
from api.services.image import Image
from api.services.serializer import Serializer
from api.services.sort import Sort
from api.services.tasks import Tasks
from api.services.validation.archive import FileArchiveValidator
from api.services.validation.dataset import FileDatasetValidator
from api.services.validation.file import FileSelectValidator, FileListValidator, FilePathValidator
from api.services.validation.visualisation import FileVisualisationValidator, FilePathValidator as FileVisualisationPathValidator
from api.services.validation.copy import FileCopyValidator
from api.services.validation.delete import FileDeletionValidator
from api.services.validation.download import FileDownloadValidator
from api.services.validation.sort import FileSortValidator
from api.visualisation.visualisation import Visualisation

@file_api.route('/select', methods=['POST'])
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

    task = current_app.config["FILE_WORKER"].send_task(f'{current_app.import_name}.process_file_select', args=[data], kwargs={})
    Tasks().write_file(task.id, url_for('file.file_check_progress', task_id = task.id, external=True), data)
    return jsonify({
        'url': f"{url_for('file.file_check_progress', task_id = task.id, external=True)}",
        'task_id': task.id
    })

@file_api.route('/download/<string:task_name>', defaults = {'format': 'csv'}, methods=['GET'])
@file_api.route('/download/<string:task_name>/<string:format>', methods=['GET'])
def file_download(task_name: str, format: str):
    content_type = ContentType()
    if not content_type.validate(format): return jsonify({"error": "1", "message": f"File format not supported: {format}."}), 400 
    serialised_data = current_app.config["CACHE"].get(f"processed_images_{task_name}")
    if serialised_data is None: return jsonify({"error": "1", "message": f"Data not found for task: {task_name}."}), 404 

    deserialised_data = Serializer().deserialize(serialised_data)
    data_file = content_type.convert_df(deserialised_data, format)
    res = make_response(data_file)
    res.headers["Content-Disposition"] = f"attachment; filename={task_name}.{format}"
    res.headers["Content-Type"] = content_type.get_content_type(format)
    return res

@file_api.route('/download', methods=['POST'])
def file_download_to_dir():
    validator = FileDownloadValidator()
    data = validator.validate(request)
    if data is None: return jsonify(validator.get_error_message()), 400 

    content_type = ContentType()
    if not content_type.validate(data["format"]): return jsonify({"error": "1", "message": f"File format not supported: {data['format']}."}), 400 
    serialised_data = current_app.config["CACHE"].get(f"processed_images_{data['task']}")
    if serialised_data is None: return jsonify({"error": "1", "message": f"Data not found for task: {data['task']}."}), 404 

    deserialised_data = Serializer().deserialize(serialised_data)
    df, out = content_type.write_df(deserialised_data, data["task"], data["format"], data["out"])

    return jsonify({
        "status": "complete",
        "out": out
    })

@file_api.route('/visualisation/<string:method>/<string:task_name>', methods=['GET'])
def file_visualisation_by_task(method: str, task_name: str):
    visualisation = Visualisation()
    if not visualisation.validate(method): return jsonify({"error": "1", "message": f"Visualisation method not supported: {method}."}), 400 

    serialised_data = current_app.config["CACHE"].get(f"processed_images_{task_name}")
    if serialised_data is None: return jsonify({"error": "1", "message": f"Data not found for task: {task_name}."}), 404 

    deserialised_data = Serializer().deserialize(serialised_data)
    plot = visualisation.visualise(method, deserialised_data)
    return jsonify(plot)

@file_api.route('/visualisation', methods=['POST'])
def file_visualisation_by_file():
    validator = FileVisualisationValidator()
    data = validator.validate(request)
    if data is None: return jsonify(validator.get_error_message()), 400 

    content_type = ContentType()
    if not content_type.validate(data["format"]): return jsonify({"error": "1", "message": f"File format not supported: {data['format']}."}), 400 

    visualisation = Visualisation()
    if not visualisation.validate(data["method"]): return jsonify({"error": "1", "message": f"Visualisation method not supported: {data['method']}."}), 400 

    validator = FileVisualisationPathValidator()
    data = validator.validate(data)
    if data is None: return jsonify(validator.get_error_message()), 400 

    plot = visualisation.visualise(data["method"], data["data"])
    return jsonify(plot)

@file_api.route('/sort', methods=['POST'])
def file_sort():
    validator = FileSortValidator()
    data = validator.validate(request)
    if data is None: return jsonify(validator.get_error_message()), 400 

    validator = FileVisualisationPathValidator()
    data = validator.validate(data)
    if data is None: return jsonify(validator.get_error_message()), 400 

    sort_res = Sort().sort(data["data"], data["out"])
    return jsonify(sort_res)

@file_api.route('/copy', methods=['POST'])
def file_copy():
    data = request.get_json()
    error_message = {"error": 1, "message": "Invalid request body format.", "permitted format": { "in": "/file/path", "out": "/file/path" }}
    if data is None: return jsonify(error_message), 400
    if "in" not in data or "out" not in data: return jsonify(error_message), 400
    
    error_message["message"] = "Supplied file does not exist."
    if not os.path.exists(data["in"]): return jsonify(error_message), 400
    copy = Copy().copy(data["in"], data["out"])

    error_message["message"] = f"Copy failed: {data['in']}"
    if copy:
        return jsonify({
            "status": "complete",
            "in": data["in"],
            "out": data["out"]
        })
    else: return jsonify(error_message)

@file_api.route('/copy/data', methods=['POST'])
def file_copy_data():
    validator = FileCopyValidator()
    data = validator.validate(request)
    if data is None: return jsonify(validator.get_error_message()), 400 
    
    content_type = ContentType()
    df, out = content_type.write_df_to_out(data["data"], data["out"], data["out_format"])

    return jsonify({
        "status": "complete",
        "in": data["in"],
        "out": out
    })

@file_api.route('/archive', methods=['POST'])
def file_archive():
    validator = FileArchiveValidator()
    data = validator.validate(request)
    if data is None: return jsonify(validator.get_error_message()), 400 
    archive = Archiver().process(data["task"], data["type"], data["in"], data["out"])
    if archive:
        return jsonify({
            "status": "complete",
            "in": data["in"],
            "out": data["out"]
        })
    else:
        return jsonify({"error": 1, "message": "Archive failed.", "in": data["in"], "out": data["out"]}), 400

@file_api.route('/delete', methods=['DELETE'])
def file_delete():
    deletion_validator = FileDeletionValidator()
    data = deletion_validator.validate(request)
    if data is None: return jsonify(deletion_validator.get_error_message()), 400 
    deletions = Deletion().delete_multiple(data["files"])
    return jsonify({
        "status": "complete",
        "files": deletions
    })

@file_api.route('/check_progress/<string:task_id>', methods=['GET'])
def file_check_progress(task_id: str):
    job = current_app.config["FILE_WORKER"].AsyncResult(task_id)
    if job.state == states.PENDING: return jsonify({"status": "pending"}), 202
    elif job.state == states.SUCCESS: return jsonify(job.result)
    elif job.state == "PROGRESS":
        res = {
            "status": "progress",
            "step": job.result["step"],
            "step_num": job.result['step_num'],
            "step_total": job.result['step_total'],
            "substeps": job.result["substeps"]
        }
        if res["substeps"] == 1:
            res["substep"] = job.result["substep"],
            res["substep_num"] = job.result['substep_num']
            res["substep_total"] = job.result['substep_total']
        return jsonify(res), 202 
    else: return jsonify({"status": "error"}), 500

@file_api.route('/images', methods=['POST'])
def file_view_images():
    data = request.get_json()
    error_message = "Invalid image path provided."
    permitted_format =  { "path": "/image/path"}
    if data is None: return jsonify({"error": 1, "Message": error_message, "permitted format": permitted_format}), 400
    if "path" not in data: return jsonify({"error": 1, "Message": error_message, "permitted format": permitted_format}), 400
    if not os.path.isdir(data["path"]): return jsonify({"error": 1, "Message": error_message, "permitted format": permitted_format}), 400

    processed_directory = Image().process_directory(data["path"])
    return jsonify(processed_directory)

@file_api.route('/datasets', methods=['POST'])
def file_view_datasets():
    data = request.get_json()
    error_message = "Invalid dataset path provided."
    permitted_format =  { "path": "/dataset/path"}
    if data is None: return jsonify({"error": 1, "Message": error_message, "permitted format": permitted_format}), 400
    if "path" not in data: return jsonify({"error": 1, "Message": error_message, "permitted format": permitted_format}), 400
    if not os.path.isdir(data["path"]): return jsonify({"error": 1, "Message": error_message, "permitted format": permitted_format}), 400

    processed_directory = Dataset().process_directory(data["path"])
    return jsonify(processed_directory)

@file_api.route('/tasks', methods=['POST'])
def file_view_tasks():
    data = request.get_json()
    error_message = "Invalid tasks path provided."
    permitted_format =  { "path": "/dataset/path"}
    if data is None: return jsonify({"error": 1, "Message": error_message, "permitted format": permitted_format}), 400
    if "path" not in data: return jsonify({"error": 1, "Message": error_message, "permitted format": permitted_format}), 400
    if not os.path.isdir(data["path"]): return jsonify({"error": 1, "Message": error_message, "permitted format": permitted_format}), 400

    processed_directory = Tasks().process_directory(data["path"])
    return jsonify(processed_directory)    

@file_api.route('/image/<path:path>', methods=['GET'])
def file_view_image(path):
    return send_file(f"/{path}")

@file_api.route('/dataset/view', methods=['POST'])
def file_view_dataset():
    validator = FileDatasetValidator()
    data = validator.validate(request)
    if data is None: return jsonify(validator.get_error_message()), 400 
    return jsonify(data["data"])

@file_api.route('/options', methods=['GET', 'POST', 'PUT'])
def file_options():
    if request.method == "GET": return jsonify(current_app.config["OPTIONS"].get())
    elif request.method == "POST": return jsonify(current_app.config["OPTIONS"].reset())
    else:
        options =  current_app.config["OPTIONS"].update_from_request(request)
        if options is None: return jsonify({"error": 1, "message": "Invalid options provided."}), 400
        return jsonify(options)


