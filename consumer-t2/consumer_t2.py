import json
import base64
# import requests


def lambda_handler(event, context):
    print('EVENTS:', event)
    messages = [event['records'][key][0]['value'] for key in event['records'].keys()]
    messages = [message.encode('utf-8') for message in messages]
    messages = [base64.decodebytes(message) for message in messages]
    messages = [eval(message) for message in messages] # json objects you can write to dynamodb
    
    
    print('processed messages:', messages)
    

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Messages Received",
            
        }),
    }
