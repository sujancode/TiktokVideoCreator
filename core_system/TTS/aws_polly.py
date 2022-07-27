#!/usr/bin/env python3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound
import sys
import random
from dotenv import load_dotenv
import os

load_dotenv()

voices = [
    "Brian",
    "Emma",
    "Russell",
    "Joey",
    "Matthew",
    "Joanna",
    "Kimberly",
    "Amy",
    "Geraint",
    "Nicole",
    "Justin",
    "Ivy",
    "Kendra",
    "Salli",
    "Raveena",
]


class AWSPolly:
    def __init__(self):
        self.max_chars = 0
        self.voices = voices

    def run(self, text, filepath, voice="Matthew"):
        try:
            AWSAccessKeyId=os.environ["AWSAccessKeyId"]
            AWSSecretKey=os.environ["AWSSecretKey"]

            session = Session(aws_access_key_id=AWSAccessKeyId,aws_secret_access_key=AWSSecretKey,region_name="us-east-1")
            polly = session.client("polly")
            voice=voice.capitalize()

            try:
                # Request speech synthesis
                response = polly.synthesize_speech(
                    Text=text, OutputFormat="mp3", VoiceId=voice, Engine="neural"
                )

            except (BotoCoreError, ClientError) as error:
                # The service returned an error, exit gracefully
                print(error)
                sys.exit(-1)

            # Access the audio stream from the response
            if "AudioStream" in response:
                file = open(filepath, "wb")
                file.write(response["AudioStream"].read())
                file.close()
                # print_substep(f"Saved Text {idx} to MP3 files successfully.", style="bold green")

            else:
                # The response didn't contain audio data, exit gracefully
                print("Could not stream audio")
                sys.exit(-1)
        except ProfileNotFound:
            print("You need to install the AWS CLI and configure your profile")
            print(
                """
            Linux: https://docs.aws.amazon.com/polly/latest/dg/setup-aws-cli.html
            Windows: https://docs.aws.amazon.com/polly/latest/dg/install-voice-plugin2.html
            """
            )
            sys.exit(-1)

    def randomvoice(self):
        return random.choice(self.voices)
