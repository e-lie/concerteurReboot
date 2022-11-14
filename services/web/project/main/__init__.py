import os

from flask import Blueprint, render_template, jsonify, send_from_directory, request, current_app
from werkzeug.utils import secure_filename

#from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route("/")
def hello_world():
    return jsonify(hello="world")


@main.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(current_app.config["STATIC_FOLDER"], filename)


@main.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(current_app.config["MEDIA_FOLDER"], filename)


@main.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config["MEDIA_FOLDER"], filename))
    return """
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """