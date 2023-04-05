import os
import time
import subprocess
from datetime import datetime, timedelta

from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play

from ..models import Question, Message

from .. import scheduler
from .. import db


# def preload_sounds(current_app):
#     with current_app.app_context():
#         current_app.sound_dict = {}
#         questions = db.session.query(Question)
#         for question in questions:
#             current_app.sound_dict[f"{question.base_filename}.wav"] = AudioSegment.from_wav(f"{current_app.config['MP3_FOLDER']}/{question.base_filename}.wav")
#         messages = db.session.query(Message)
#         for message in messages:
#             current_app.sound_dict[f"{message.base_filename}.wav"] = AudioSegment.from_wav(f"{current_app.config['MP3_FOLDER']}/{message.base_filename}.wav")
#     print(current_app.sound_dict)


def play_sound_scenario(current_app, scenario_name="question_random_message", message_amount=5, pause_time=0.2):
    # preload_sounds(current_app)
    with current_app.app_context():
        current_app.sound_dict = {}
        questions = db.session.query(Question)
        for question in questions:
        # play(audio_segment)
            subprocess.run(["aplay", f"{current_app.config['MP3_FOLDER']}/{question.base_filename}.wav"])
            # current_app.sound_dict[f"{question.base_filename}.wav"] = AudioSegment.from_wav(f"{current_app.config['MP3_FOLDER']}/{question.base_filename}.wav")
    # for name, audio_segment in current_app.sound_dict.items():

    # with current_app.app_context():
    #     currQuestion = db.session.query(Question).filter(Question.current == True).first()
    #     if not currQuestion:
    #         return

    #     sounds = []
    #     for message in currQuestion.messages:
    #         if message.base_filename:
    #             sounds.append(current_app.sound_dict[f"{message.base_filename}.wav"])
    #             # try:
    #             #     # playsound(f"{current_app.config['MP3_FOLDER']}/{message.base_filename}.wav")
    #             #     # sound = AudioSegment.from_wav(f"{current_app.config['MP3_FOLDER']}/{message.base_filename}.wav")
    #             #     # play(sound)
    #             # except Exception as e:
    #             #     print("Error playing sound")
        
    #     for sound in sounds:
    #         play(sound)
    #         # time.sleep(pause_time)

@scheduler.task(
    "interval",
    id="job_player",
    seconds=0.1,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def gpio_player():
    if scheduler.app.gpio_button:
        if scheduler.app.gpio_button.is_pressed: 
            print("Button is pressed")
            # subprocess.run(["aplay", f"{scheduler.app}1_test_2023-03-16T17-44-36-578546-00-00.wav"])
            play_sound_scenario(current_app=scheduler.app)

# @scheduler.task(
#     "interval",
#     id="job_preload_sounds",
#     seconds=10,
#     max_instances=1,
#     start_date="2000-01-01 12:19:00",
# )
# def preload_sounds_job():
#     preload_sounds(current_app=scheduler.app)
