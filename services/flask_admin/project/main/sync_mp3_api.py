from flask import jsonify, request, current_app, url_for, redirect
from flask_login import login_required

from .. import db
from ..models import Question
from . import main

import parse

@main.route('/update-status', methods=['POST'])
@login_required
def update_status():
    print(current_app.config['UPDATE_STATUS'])
    signature = request.form['signature']
    if (current_app.config['UPDATE_STATUS'] and
            signature not in current_app.config['CLIENT_STACK']):
        current_app.config['CLIENT_STACK'].append(signature)
        if len(current_app.config['CLIENT_STACK']) >= current_app.config['CLIENT_NUMBER']:
            current_app.config['UPDATE_STATUS'] = False
            current_app.config['CLIENT_STACK'] = []
        data = {'update_status': True}
    else:
        data = {'update_status': False}
    return jsonify(data)


@main.route('/set-refresh', methods=['GET'])
@login_required
def set_refresh():
    current_app.config['UPDATE_STATUS'] = True
    return redirect(url_for('.messages'))


@main.route('/get-sound-list', methods=['POST'])
@login_required
def get_sound_list():
    refresh = request.form['refresh']
    if refresh == "True":
        refresh = True
    else:
        refresh = False
    current_question = db.session.query(Question).filter(Question.current == True).first()
    message_ids = [int(message.id) for message in current_question.messages]

    lastfilename = request.form['lastFilename']
    if lastfilename:
        message_id = int(parse.parse("{}_{}_{}", lastfilename)[0])
    else:
        message_id = 1

    if refresh or (message_id not in message_ids):
        filename_list = [message.base_filename+'.mp3' for message in current_question.messages]
        if filename_list:
            data = {'filenames': filename_list, 'lastfilename': filename_list[-1], 'refresh': True,
                    'question_active': current_app.config['QUESTION_ACTIVE'],
                    'question_filename': current_question.base_filename+'.mp3'}
        else:
            data = {'filenames': filename_list, 'lastfilename': lastfilename, 'refresh': True,
                    'question_active': current_app.config['QUESTION_ACTIVE'],
                    'question_filename': current_question.base_filename+'.mp3'}
    else:
        messages_ids_to_dl = [i for i in message_ids if i > message_id]
        filenames_to_dl = [message.base_filename+'.mp3' for message in current_question.messages if
                           message.id in messages_ids_to_dl]
        if filenames_to_dl:
            data = {'filenames': filenames_to_dl, 'lastfilename': filenames_to_dl[-1], 'refresh': False,
                    'question_active': current_app.config['QUESTION_ACTIVE'], 'question_filename': ''}
        else:
            data = {'filenames': filenames_to_dl, 'lastfilename': lastfilename, 'refresh': False,
                    'question_active': current_app.config['QUESTION_ACTIVE'], 'question_filename': ''}

    return jsonify(data)


# if int(message_id) < 0:
#     message_id = 1

# print("get_sound_list -> message_id : " + str(message_id))

# max_id = int(db.session.query(Message.id).order_by(Message.id.desc()).first()[0])

# print("get_sound_list -> max_id : " + str(max_id))
# if int(message_id) > max_id:
#     message_id = 1
#     filename = "{}_mfoaiezjfamozife_moiefamoiezjf".format(max_id)

# question_elem = db.session.query(Message.question_id).filter(Message.id == message_id).first()
# question_id = -1
# if question_elem:
#     question_id = int(question_elem[0])
# current_question = db.session.query(Question).filter(Question.current==True).first()

# print(current_question.id)
# print(question_id)
# if question_id < current_question.id:
#     new_question = True
#     filename_list = [message.base_filename+'.mp3' for message in current_question.messages]
# else:
#     new_question = False
#     filename_tuples = db.session.query(Message.base_filename+'.mp3').filter(Message.id > message_id).all()
#     filename_list = [tupl[0] for tupl in filename_tuples]
#     print(filename_list)

#
# if filename_list:
#     data = { 'new_question':new_question, 'filenames':filename_list, 'lastfilename':filename_list[-1]}
# else:
#     data = { 'new_question':new_question, 'filenames':filename_list, 'lastfilename':filename}
#     print(jsonify(data))
# return jsonify(data)

@main.route('/get-sound', methods=['POST'])
@login_required
def get_sound():
    filename = request.form['soundname']
    mp3Url = 'mp3' + '/' + filename
    return main.send_static_file(mp3Url)