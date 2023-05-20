import os
import time
import subprocess
import pygame
from datetime import datetime, timedelta
from random import shuffle
from time import sleep

from ..models import Question, Message

from .. import scheduler
from .. import db

display=pygame.display.set_mode((1000,700))
pygame.init()

def play_sound_scenario(current_app, playing_question=False, playing_random_message=True, message_amount=5, play_interval=0.5, maxtime=2000):
    with current_app.app_context():

        current_question = db.session.query(Question).filter(Question.current == True).first()
        all_message_sound_paths = [
            f"{current_app.config['MP3_FOLDER']}/{message.base_filename}.wav"
            for message in current_question.messages
        ]

        # try:
        all_message_sounds = [pygame.mixer.Sound(sound_path) for sound_path in all_message_sound_paths]
        question_sound = pygame.mixer.Sound(f"{current_app.config['MP3_FOLDER']}/{current_question.base_filename}.wav")
        if current_app.config["virgule1_filename"]:
            virgule1 = pygame.mixer.Sound(f"{current_app.config['VIRGULES_FOLDER']}/{current_app.config['virgule1_filename']}")
        if current_app.config["virgule2_filename"]:
            virgule2 = pygame.mixer.Sound(f"{current_app.config['VIRGULES_FOLDER']}/{current_app.config['virgule2_filename']}")
        # except:
            # print(f"Error loading one of the sound files")
            # return

        print(all_message_sounds)

        if current_app.config["virgule1_filename"]:
            virgule1.play(fade_ms=200, maxtime=maxtime)
            sleep(min(virgule1.get_length(), maxtime/1000))
        sleep(play_interval/1000)
        if playing_question:
            question_sound.play(fade_ms=200)
            sleep(question_sound.get_length())
            if current_app.config["virgule2_filename"]:
                sleep(play_interval/1000)
                virgule2.play(fade_ms=200, maxtime=maxtime)
                sleep(min(virgule2.get_length(), maxtime/1000))
            sleep(play_interval/1000)

        if playing_random_message:
            shuffle(all_message_sounds)

        messages_to_play = all_message_sounds[:message_amount]

        for i,message_sound in enumerate(messages_to_play):
            if i > 0 and current_app.config["virgule2_filename"]: # don't play before first message
                sleep(play_interval/1000)
                virgule2.play(fade_ms=200, maxtime=maxtime)
                sleep(min(virgule2.get_length(), maxtime/1000))
            message_sound.play(fade_ms=200)
            sleep(message_sound.get_length())
            sleep(play_interval/1000)

        if current_app.config["virgule1_filename"]:
            virgule1.play(fade_ms=200, maxtime=maxtime)
            sleep(min(virgule1.get_length(), maxtime/1000))


@scheduler.task(
    "interval",
    id="job_player",
    seconds=0.1,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def gpio_player():
    # print(scheduler.app.config)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not scheduler.app.config['play_triggered']:
                    scheduler.app.config['play_triggered'] = True
                    print("buttttoooonn")
                    scheduler.app.config['num_messages_to_play']=5
                    scheduler.app.config['play_interval']=0.2
                    scheduler.app.config['random_play'] = True
                    scheduler.app.config['play_question'] = True
                    scheduler.app.config['virgule1_filename'] = "virgule3.wav"
                    scheduler.app.config['virgule2_filename'] = "virgule4.wav"
                    play_sound_scenario(
                        current_app=scheduler.app,
                        message_amount=scheduler.app.config['num_messages_to_play'],
                        play_interval=scheduler.app.config['play_interval'],
                        playing_random_message=scheduler.app.config['random_play'],
                        playing_question=scheduler.app.config['play_question'],
                    )
                    scheduler.app.config['play_triggered'] = False
