import os

# https://github.com/olucurious/PyFCM

from pyfcm import FCMNotification

api_key = os.environ.get('FCM_API_KEY'),
push_service = FCMNotification(api_key="api_key")


def send_messages(registration_ids: list, title: str, body: str, dataDict: dict = None):
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=title,
                                                  message_body=body, data_message=dataDict)
    if result:
        if result['failure'] == 0:
            print(result)
    # TODO: Need to save result in log file also can trigger a mail to developer
