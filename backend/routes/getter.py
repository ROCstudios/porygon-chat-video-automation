from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
import shutil
import time
from cloud_storage import all_files_from_gcs

getter_routes = Blueprint('getter', __name__)

@getter_routes.route('/audios', methods=['GET'])
def get_audios():
    return jsonify({"audios": all_files_from_gcs()}), 200
