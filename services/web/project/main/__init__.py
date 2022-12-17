

#from flask_login import login_required, current_user

from flask import Blueprint

main = Blueprint('main', __name__, static_folder='../static', template_folder='templates')

from . import admin
from . import sync_mp3_api



# @main.route("/static/<path:filename>")
# def staticfiles(filename):
#     return send_from_directory(current_app.config["STATIC_FOLDER"], filename)


# @main.route("/media/<path:filename>")
# def mediafiles(filename):
#     return send_from_directory(current_app.config["MEDIA_FOLDER"], filename)


# @main.route("/upload", methods=["GET", "POST"])
# def upload_file():
#     if request.method == "POST":
#         file = request.files["file"]
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(current_app.config["MEDIA_FOLDER"], filename))
#     return """
#     <!doctype html>
#     <title>upload new File</title>
#     <form action="" method=post enctype=multipart/form-data>
#       <p><input type=file name=file><input type=submit value=Upload>
#     </form>
#     """