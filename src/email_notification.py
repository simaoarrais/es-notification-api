import logging
import json
import os
import json
import boto3

from time import time

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_notification(body):

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

    ALERT_EMAIL_FROM = os.environ.get('ALERT_EMAIL_FROM', '')
    ALERT_EMAIL_TO = os.environ.get('ALERT_EMAIL_TO', '').split(',')

    message = {
            'camera_id': body['camera_id'],
            'frame_timestamp': body['frame_timestamp'],
            'trigger_timestamp': time()
        }

    message = json.dumps({'default': json.dumps(message)})
    print("Publish Message: " + message)

    email_ses_client = boto3.client(
        "ses",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="eu-west-3"
    )

    # Provide the contents of the email.
    send_args = {
        'Source': ALERT_EMAIL_FROM,
        'Destination': {'ToAddresses': ALERT_EMAIL_TO},
        'Message': {
            'Subject': {'Data': 'An intrusion has been detected through camera ' + str(body['camera_id'])},
            'Body': {'Text': {'Data': message}}
        }
    }

    response = email_ses_client.send_email(**send_args)

    return response
    