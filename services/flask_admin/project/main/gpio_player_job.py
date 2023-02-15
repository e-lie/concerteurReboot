import os
import time
from datetime import datetime, timedelta

from playsound import playsound

from ..models import Question, Message

from .. import scheduler
from .. import db


def play_sound_scenario(current_app, scenario_name="question_random_message", message_amount=5, pause_time=1):
    
    with current_app.app_context():
        currQuestion = db.session.query(Question).filter(Question.current == True).first()
        if not currQuestion:
            return

        for message in currQuestion.messages:
            if message.base_filename:
                playsound(f"{current_app.config['MP3_FOLDER']}/{message.base_filename}.mp3")
                time.sleep(pause_time)





@scheduler.task(
    "interval",
    id="job_player",
    seconds=10,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def gpio_player():
    
    if scheduler.app.gpio_button:
        print(scheduler.app.gpio_button)

    play_sound_scenario(current_app=scheduler.app)
