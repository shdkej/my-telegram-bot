#-*- coding:utf-8 -*-
import json
import os
from botocore.vendored import requests
import logging

CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps('ok')
}
ERROR_RESPONSE = {
        'statusCode': 400,
        'body': json.dumps('Ooops')
        }


def hello(event, context):
    logger.info('Event: {}'.format(event))

    if event.get('httpMethod') == 'POST' and event.get('body'):
        logger.info('Message received')
        load_data = json.loads(event["body"])
        message = str(load_data["message"]["text"])

        response = message

        if "start" in message:
            response = "Hello"

        send_message(response)

        return OK_RESPONSE
    elif event.get('Records'):
        logger.info('SQS Message received')
        message = event["Records"][0]['body']

        response = message
        if message.find("responsePayload") != -1:
            load_data = json.loads(message)
            response = load_data['responsePayload']['message']

        logger.info(response)
        send_message(response)

        return OK_RESPONSE
        
    return ERROR_RESPONSE


def send_message(message):
    url = BASE_URL + "/sendMessage"
    strMessage = message
    if type(message) == list:
        strMessage = ''
        for m in message:
            strMessage += m
            strMessage += "\n"
    data = {"text": strMessage.encode("utf8"), "chat_id": CHAT_ID}
    requests.post(url, data)
