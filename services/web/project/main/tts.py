import os
from urllib import request, parse
from boto3 import client, Session
from contextlib import closing


def amazon_polly_tts(message, voice_id='Celine'):
    session = Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET"),
        region_name=os.getenv("AWS_REGION")
    )

    polly = session.client("polly")

    response = polly.synthesize_speech(
        Text=message,
        OutputFormat="mp3",
        VoiceId=voice_id
    )

    with closing(response["AudioStream"]) as stream:
        mp3_sound = stream.read()
        return mp3_sound
