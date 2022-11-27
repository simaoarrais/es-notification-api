import json
from src.sms_notification import send_notification
from unittest import mock
from twilio.base.exceptions import TwilioRestException



@mock.patch('src.sms_notification.client.messages.create')
def test_send_notification(create_message_mock):
    """
    Mocks and tests the API Client 
    """
    
    #Mock the API
    expected_sid = 'SM87105da94bff44b999e4e6eb90d8eb6a'
    create_message_mock.return_value.sid = expected_sid

    #Create message request
    message = {
        "phone_number": "+351968767989",
        "message": "You have 1 intruder on camera 2"
    }
    message = json.dumps(message)
    sid = send_notification(message)

    #Check if Mock was called
    assert create_message_mock.called is True
    #Check if sid matched
    assert sid == expected_sid


@mock.patch('src.sms_notification.client.messages.create')
def test_error_invalid_json_send_notification(create_message_mock):
    """
    Mocks the API Client and tests Exception in case of invalid JSON parameter
    """

    #Mock the API
    expected_sid = None
    create_message_mock.return_value.sid = expected_sid

    #Create error_message
    error_message = {
        "phone_number": "+351968767989",
        "message": "You have 1 intruder on camera 2"
    }
    sid = send_notification(error_message)

    #Check if method returned None
    assert sid == expected_sid

@mock.patch('src.sms_notification.client.messages.create')
def test_error_send_notification(create_message_mock, caplog):
    """
    Mocks the API Client and tests Exception in case of internal server error on API
    """

    #Create message
    message = {
        "phone_number": "+351968767989",
        "message": "You have 1 intruder on camera 2"
    }
    message = json.dumps(message)

    #Mock API
    status = 500
    uri = '/Accounts/ACXXXXXXXXXXXXXXXXX/Messages.json'
    create_message_mock.side_effect = TwilioRestException(status, uri, msg=message)

    sid = send_notification(message)

    #Check if the expected message is logged and the method returns None
    assert sid is None
    assert 'Unexpected Error:' in caplog.text
    assert message in caplog.text
