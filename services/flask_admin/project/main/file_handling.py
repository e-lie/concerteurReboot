import os
import shutil


def write_mp3_sound(entry, mp3_sound, current_app): # For question or message
    if not os.path.exists(current_app.config['MP3_FOLDER']): # ensure question archive directory exists
        os.makedirs(current_app.config['MP3_FOLDER'])
    with open(f"{current_app.config['MP3_FOLDER']}/{entry.base_filename}.mp3", 'wb+') as mp3:
        mp3.write(mp3_sound)


def create_question_archive(question, mp3_sound, current_app):
    '''
    Create a zip archive for the question to be downloaded.
    Zip directory for the question with mp3 sound, question text plus sound and text from the associated messages
    '''
    question_archive_path = '{}/{}/'.format(current_app.config['ARCHIVE_FOLDER'], question.base_filename)

    if not os.path.exists(question_archive_path): # ensure question archive directory exists
        os.makedirs(question_archive_path)

    with open(question_archive_path + question.base_filename + ".mp3" , 'wb+') as archive_mp3:
        archive_mp3.write(mp3_sound)

    with open(question_archive_path + question.base_filename + ".txt" , 'a') as messages_file:
        messages_file.write('Question : {}\n\n{}\n\n{}\n------\n'.format(question.title, question.base_filename + ".mp3", question.text))

    rezip_question_archive(question, current_app)


def add_message_to_question_archive(message, question, mp3_sound, current_app):
    question_archive_path = '{}/{}/'.format(current_app.config['ARCHIVE_FOLDER'], question.base_filename)

    with open(question_archive_path + "message_" + message.base_filename + ".mp3", 'wb+') as archive_mp3:
        archive_mp3.write(mp3_sound)
    with open(question_archive_path + "message_" + current_app.config["MESSAGES_ARCHIVE_FILENAME"] + ".txt", 'a') as messages_file:
        messages_file.write('{}\n\n{}\n------\n'.format(message.base_filename+'.mp3', message.text))

    rezip_question_archive(question, current_app)


def rezip_question_archive(question, current_app):
    question_archive_path = f'{current_app.config["ARCHIVE_FOLDER"]}/{question.base_filename}'
    shutil.make_archive(question_archive_path, 'zip', current_app.config['ARCHIVE_FOLDER'] + '/' + question.base_filename)
