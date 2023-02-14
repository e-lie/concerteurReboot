import os
from datetime import datetime, timedelta

from playsound import playsound

from .. import scheduler
from .. import db



@scheduler.task(
    "interval",
    id="job_player",
    seconds=0.1,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def gpio_player():

    # playsound(f"{scheduler.app.config['MP3_FOLDER']}/1_2023-02-14T10:17:50.027725+00:00_7752727703425084533.mp3")

    with scheduler.app.app_context():
        print(scheduler.app.gpio_button)
        if scheduler.app.gpio_button.is_pressed: 
            print("Button is pressed yaaaaa !!!!!!") 
    #     currQuestion = db.session.query(Question).filter(Question.current == True).first()
    #     if not currQuestion:
    #         return
