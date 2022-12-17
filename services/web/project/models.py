from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)

    #ajust the datetime entry from the clock of the db server. Better because it can be different from the app server's one
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    title = db.Column(db.Unicode(300))
    text = db.Column(db.Unicode(1000))
    current = db.Column(db.Boolean())
    #archive_name = db.Column(db.Unicode(300))
    base_filename = db.Column(db.String(500))
    trashed = db.Column(db.Boolean(), default=False)

    messages = db.relationship('Message', backref='question')


    def __init__(self, text, title, current):
        self.text = text
        self.title = title
        self.current = current

    def __repr__(self):
        return '<Question {}: {}>'.format(self.id, self.text)

class Contributor(db.Model):
    __tablename__ = 'contributors'
    id = db.Column(db.Integer, primary_key=True)
    phone_number_hash = db.Column(db.String(100))
    messages = db.relationship('Message', backref='contributor')

    def __init__(self, numHash, message):
        self.phone_number_hash = numHash
        self.messages = [message]

    def __repr__(self):
        return '<Contributor {}: {}>'.format(self.id, self.phone_number_hash)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    
    #ajust the 7datetime entry from the clock of the db server. Better because it can be different from the app server's one
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    contributor_id = db.Column(db.Integer, db.ForeignKey('contributors.id'))
    text = db.Column(db.Unicode(1000))
    base_filename = db.Column(db.String(500))
    trashed = db.Column(db.Boolean(), default=False)

    def __init__(self, text, question_id):
        self.text = text
        self.question_id = question_id

    def __repr__(self):
        return '<Message {}: {}>'.format(self.id, self.text)
