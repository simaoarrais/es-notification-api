import logging
import json
import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_notification(body):
    """
    Given a Json body, sends a WhatsApp notification.

    Parameters
    ----------
        body : JSON
            Contains the contents of the body notification to be sent
    
    Returns:
    ----------
        sid : Str
            Unique Whatsapp message ID composed by 34 char string starting with SM

    Exception:
    ----------
        TypeError: The JSON object must be str, bytes or bytearray, not dict
        TwilioRestException: API call error
    """

    # Authentication for Twilio
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Open body as Json object
    try:
        body_json = json.loads(body)
    except (TypeError) as e:
        logging.error(f"Invalid Json body: {e}")
        return None

    # Make API call to send notification
    try:
        message_properties = client.messages.create( 
            from_ = 'whatsapp:+14155238886',       
            to = f'whatsapp:{body_json["phone_number"]}',
            body = body_json["message"]
        )
    except TwilioRestException as e:
        logging.error(f"Unexpected Error: {e}")
        return None

    return message_properties.sid
    