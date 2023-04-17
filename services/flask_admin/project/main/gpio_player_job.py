import os
import time
import subprocess
from datetime import datetime, timedelta
from random import shuffle
from time import sleep

from ..models import Question, Message

from .. import scheduler
from .. import db


def play_sound_scenario(current_app, playing_question=False, playing_random_message=True, message_amount=5, play_interval=0.5):
    with current_app.app_context():
        current_question = db.session.query(Question).filter(Question.current == True).first()
        all_message_sound_paths = [
            f"{current_app.config['MP3_FOLDER']}/{message.base_filename}.wav"
            for message in current_question.messages
        ]

        print(all_message_sound_paths)

        if current_app.config["virgule1_filename"]:
            try:
                subprocess.run(["aplay", f"{current_app.config['VIRGULES_FOLDER']}/{current_app.config['virgule1_filename']}"])
            except:
                print(f"error playing virgule1 {current_app.config['VIRGULES_FOLDER']}/{current_app.config['virgule1_filename']}")
            sleep(play_interval)

        if playing_question:
            subprocess.run(["aplay", f"{current_app.config['MP3_FOLDER']}/{current_question.base_filename}.wav"])
            sleep(play_interval)
            if current_app.config["virgule2_filename"]:
                try:
                    subprocess.run(["aplay", f"{current_app.config['VIRGULES_FOLDER']}/{current_app.config['virgule2_filename']}"])
                except:
                    print(f"error playing virgule2 {current_app.config['VIRGULES_FOLDER']}/{current_app.config['virgule2_filename']}")
                sleep(play_interval)

        if playing_random_message:
            shuffle(all_message_sound_paths)

        messages_to_play = all_message_sound_paths[:message_amount]

        for i,message_sound_path in enumerate(messages_to_play):
            if i > 0 and current_app.config["virgule2_filename"]: # don't play before first message
                try:
                    subprocess.run(["aplay", f"{current_app.config['VIRGULES_FOLDER']}/{current_app.config['virgule2_filename']}"])
                except:
                    print(f"error playing virgule2 {current_app.config['VIRGULES_FOLDER']}/{current_app.config['virgule2_filename']}")
                sleep(play_interval)
            subprocess.run(["aplay", message_sound_path])
            sleep(play_interval)

        if current_app.config["virgule1_filename"]:
            try:
                subprocess.run(["aplay", f"{current_app.config['VIRGULES_FOLDER']}/{current_app.config['virgule1_filename']}"])
            except:
                print(f"error playing virgule1 {current_app.config['VIRGULES_FOLDER']}/{current_app.config['virgule1_filename']}")


@scheduler.task(
    "interval",
    id="job_player",
    seconds=0.1,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def gpio_player():
    if not scheduler.app.config['play_triggered']:
        if scheduler.app.config['gpio_button']:
            if scheduler.app.config['gpio_button'].is_pressed:
                scheduler.app.config['play_triggered'] = True
                print("buttttoooonn")
                play_sound_scenario(current_app=scheduler.app, playing_question=True)
                scheduler.app.config['play_triggered'] = False
