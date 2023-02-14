

#from flask_login import login_required, current_user

from flask import Blueprint

main = Blueprint('main', __name__, static_folder='../static', template_folder='templates')

from . import admin

def twilio_sms_poll():
    from twilio.rest import Client

    account_sid = "AC1b01fe2c67cb651302ca3c6cc061a569"
    auth_token = "b05d685439f2cdcbe2b9e936bb4b8411"

    client = Client(account_sid, auth_token)

    print("============ TWILIO SMS =============")
    for sms in client.messages.list():
        # help(sms)
        print(f"{sms.date_created} : {sms.to} -> {sms.body}")

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