import os
from datetime import datetime, timedelta

from .. import scheduler
from .. import db
from ..models import Question, Message
from .admin import add_message_generic

from twilio.rest import Client
import pytz

@scheduler.task(
    "interval",
    id="job_sync",
    seconds=10,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def twilio_sms_poll():
    with scheduler.app.app_context():
        currQuestion = db.session.query(Question).filter(Question.current == True).first()
        if not currQuestion:
            return

        account_sid = os.getenv('TWILIO_SID')
        auth_token = os.getenv('TWILIO_TOKEN')
        twilio_client = Client(account_sid, auth_token)

        for sms in twilio_client.messages.list(date_sent_after=datetime.utcnow().replace(tzinfo=pytz.UTC)-timedelta(minutes=20)): # fetch SMS sent in the last 20 minutes
            #help(sms)
            if not sms.direction == "inbound":
                continue

            already_added_message = db.session.query(Message).filter(Message.twilio_sid == sms.sid).first()
            if already_added_message:
                return

            print(f"FETCHED NEW SMS : {sms.date_created} : {sms.from_} -> {sms.body}, {sms.status}, {sms.sid}, {sms.direction}, {sms.date_sent}, {sms.date_updated}")
            add_message_generic(db, num=sms.from_, text=sms.body, twilio_sid=sms.sid)

            #print(sms.date_updated, sms.date_sent)
            #print(sms.date_updated + timedelta(hours=1) > sms.date_sent or sms.date_updated - timedelta(hours=1) > sms.date_sent)
