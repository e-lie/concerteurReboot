import os
import time
from datetime import datetime, timedelta

from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play

from ..models import Question, Message

from .. import scheduler
from .. import db


def play_sound_scenario(current_app, scenario_name="question_random_message", message_amount=5, pause_time=0.2):
    
    with current_app.app_context():
        currQuestion = db.session.query(Question).filter(Question.current == True).first()
        if not currQuestion:
            return

        sounds = []
        for message in currQuestion.messages:
            if message.base_filename:
                sounds.append(AudioSegment.from_wav(f"{current_app.config['MP3_FOLDER']}/{message.base_filename}.wav"))
                # try:
                #     # playsound(f"{current_app.config['MP3_FOLDER']}/{message.base_filename}.wav")
                #     # sound = AudioSegment.from_wav(f"{current_app.config['MP3_FOLDER']}/{message.base_filename}.wav")
                #     # play(sound)
                # except Exception as e:
                #     print("Error playing sound")
        
        for sound in sounds:
            play(sound)
            # time.sleep(pause_time)

@scheduler.task(
    "interval",
    id="job_player",
    seconds=0.1,
    max_instances=2,
    start_date="2000-01-01 12:19:00",
)
def gpio_player():
    if scheduler.app.gpio_button:
        if scheduler.app.gpio_button.is_pressed: 
            print("Button is pressed")
            play_sound_scenario(current_app=scheduler.app)
