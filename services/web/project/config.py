import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/media"

    SECRET_KEY = os.getenv("SECRET_KEY", "9OLWxNfuo83j4K4iuopO")

    TWILIO_SID = "XXXX"
    TWILIO_TOKEN = "XXXX"

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 't_ifJk2jhR,jl$0'
    QUESTION_ARCHIVE_DIR = 'question_archives'
    MP3_DIR = './app/static/mp3'
    ZIP_DIR = './app/static/zip'
    MESSAGES_ARCHIVE_FILENAME = 'messages.txt'
    UPDATE_STATUS = False
    CLIENT_STACK = []
    CLIENT_NUMBER = 1
    QUESTION_ACTIVE = 1
    
    CREDENTIALS = [
                {'loginUser':'EVAL_5349668',
                'loginPassword':'94wbhtnb'}
                ]
    CREDENTIAL_NUM = 0