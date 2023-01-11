import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/media"
    MP3_FOLDER_NAME = 'mp3'
    MP3_FOLDER = f'{STATIC_FOLDER}/{MP3_FOLDER_NAME}'
    ARCHIVE_FOLDER_NAME = 'question_archives'
    ARCHIVE_FOLDER = f'{STATIC_FOLDER}/{ARCHIVE_FOLDER_NAME}'
    MESSAGES_ARCHIVE_FILENAME = 'messages.txt'

    SECRET_KEY = os.getenv("SECRET_KEY", "9OLWxNfuo83j4K4iuopO")

    TWILIO_SID = "XXXX"
    TWILIO_TOKEN = "XXXX"

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    UPDATE_STATUS = False
    CLIENT_STACK = []
    CLIENT_NUMBER = 1
    QUESTION_ACTIVE = 1

    # # Flask APScheduler
    # JOBS = [
    #     {
    #         'id': 'job1',
    #         'func': 'project:job1',
    #         'args': (1, 2),
    #         'trigger': 'interval',
    #         'seconds': 10
    #     },
    #     {
    #         'id': 'twilio_sms_poll',
    #         'func': 'project:main:twilio_sms_poll',
    #         'args': (),
    #         'trigger': 'interval',
    #         'seconds': 10
    #     }
    # ]
    # SCHEDULER_API_ENABLED = True