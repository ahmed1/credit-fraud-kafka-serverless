import json
import base64
import boto3
from decimal import Decimal

# import requests

dynamo = boto3.resource('dynamodb')
rejected = dynamo.Table('rejected-transactions')

def to_decimal(message):
    message['amt'] = Decimal(str(float(message['amt'])))
    message['lat'] = Decimal(str(float(message['lat'])))
    message['long'] = Decimal(str(float(message['long'])))
    message['merch_lat'] = Decimal(str(float(message['merch_lat'])))
    message['merch_long'] = Decimal(str(float(message['merch_long'])))
    message['date'] = message['trans_date_trans_time']
    return message 


def lambda_handler(event, context):
    messages = [event['records'][key][0]['value'] for key in event['records'].keys()]
    messages = [message.encode('utf-8') for message in messages]
    messages = [base64.decodebytes(message) for message in messages]
    messages = [eval(message) for message in messages] # json objects you can write to dynamodb
    
    for message in messages:
        transaction = purchases.put_item(Item=to_decimal(message))
        rejected.put_item(transaction)

    
    print('processed messages:', messages)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
