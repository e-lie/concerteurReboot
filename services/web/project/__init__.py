import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from .main import main as main_blueprint


#from .models import User


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
app.register_blueprint(main_blueprint)



