import re
import os

from flask import render_template, request, current_app, url_for, redirect
from flask_login import login_required

from .. import db
from ..models import Question, Contributor, Message
from .forms import AddQuestionForm, AddMessageForm
from .tts import amazon_polly_tts
from .file_handling import create_question_archive, write_mp3_sound, add_message_to_question_archive
from . import main

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/add-question', methods=['GET', 'POST'])
@login_required
def add_question():
    question = None

    form = AddQuestionForm()
    if not form.validate_on_submit(): # the form is empty or not correct redisplay the form
        return render_template('add_question.html', form=form)

    #change current question to false before adding the new current question
    currQuestion = db.session.query(Question).filter(Question.current==True).first()
    if currQuestion:
        currQuestion.current = False
        db.session.add(currQuestion)

    question = Question(title=form.title.data, text=form.text.data, current=True)

    db.session.add(question)
    db.session.commit() # Commit question in DB to get and primary key id (used in question base_filename)

    form.title.data = ''
    form.text.data = ''

    question.base_filename = re.sub(
        '[^\w\-_]',
        '-',
        f'{question.id}_{question.title}_{question.time_created.isoformat()}'
    )

    mp3_sound = amazon_polly_tts(message=question.text, voice_id='Celine')
    write_mp3_sound(question, mp3_sound, current_app)
    create_question_archive(question, mp3_sound, current_app)

    db.session.commit() # add question base filename to the DB

    return redirect(url_for('.messages'))



@main.route('/messages')
@login_required
def messages():
    questions = db.session.query(Question).order_by(Question.time_created.desc()).all()
    return render_template('messages.html', questions=questions, current_app=current_app)


@main.route('/trash')
@login_required
def trash():
    questions = db.session.query(Question).order_by(Question.time_created.desc()).all()
    return render_template('trash.html', questions=questions, current_app=current_app)


@main.route('/add-message', methods=['GET', 'POST'])
@login_required
def add_sms():

    form = AddMessageForm()
    if request.method == 'GET':
        return render_template('add_message.html', form=form)

    question = db.session.query(Question).filter(Question.current==True).first()
    if not question:
        erreur = "Erreur : pas de question disponible pour ajouter des messages"
        print( erreur )
        return erreur

    phone_number_hash = str(hash(request.form['num'])) # would be better to install hashlib and use sha1 for this hash
    message = Message(text=request.form['text'], question_id=question.id)

    contributor = db.session.query(Contributor).filter(Contributor.phone_number_hash == phone_number_hash).first()
    if not contributor:
        contributor = Contributor(phone_number_hash, message)
    else:
        contributor.messages.append(message)

    db.session.add(contributor)
    db.session.add(message)
    db.session.commit() # Add message to DB to get the primary key id used in base filename

    #create a unique filename (id + timestamp + hash of the contributor number)
    message.base_filename = f"{message.id}_{message.time_created.isoformat()}_{contributor.phone_number_hash}"

    mp3_sound = amazon_polly_tts(message=message.text, voice_id='Mathieu')

    write_mp3_sound(message, mp3_sound, current_app)

    db.session.add(message)
    db.session.commit()

    add_message_to_question_archive(message, question, mp3_sound, current_app)

    return redirect(url_for('.messages'))



@main.route('/change_question/<message_num>', methods=['GET'])
@login_required
def change_question(message_num):
    new_question = db.session.query(Question).filter(Question.id == int(message_num)).first()
    old_question = db.session.query(Question).filter(Question.current == True).first()
    if new_question:
        new_question.current = True
        old_question.current = False
        db.session.add(new_question)
        db.session.add(old_question)
        db.session.commit()

    return redirect(url_for('.messages'))


@main.route('/trash-message/<message_num>', methods=['GET'])
@login_required
def trash_message(message_num):
    message = db.session.query(Message).filter(Message.id == message_num).first()
    message.trashed = True
    db.session.add(message)
    db.session.commit()
    return redirect(url_for('.messages'))


@main.route('/untrash-message/<message_num>', methods=['GET'])
@login_required
def untrash_message(message_num):
    message = db.session.query(Message).filter(Message.id == message_num).first()
    message.trashed = False
    db.session.add(message)
    db.session.commit()
    return redirect(url_for('.trash'))


@main.route('/del-message/<message_num>', methods=['GET'])
@login_required
def del_message(message_num):
    message = db.session.query(Message).filter(Message.id == message_num).first()
    db.session.delete(message)
    db.session.commit()
    os.remove(f"{current_app.config['MP3_FOLDER']}/{message.base_filename}.mp3")
    return redirect(url_for('.trash'))


@main.route('/activate-question', methods=['GET'])
@login_required
def activate_question():
    current_app.config['QUESTION_ACTIVE'] = 1
    return redirect(url_for('.messages'))



@main.route('/deactivate-question', methods=['GET'])
@login_required
def deactivate_question():
    current_app.config['QUESTION_ACTIVE'] = 0
    return redirect(url_for('.messages'))


