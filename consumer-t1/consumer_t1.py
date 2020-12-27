import json
import base64
# import requests


def lambda_handler(event, context):
    print('event:', event)

    message = message.encode('utf-8')
    message = base64.decodebytes(message)
    
    messages = [event['records'][x][0]['value'] for x in event['records'].keys()]
    for message in messages:
        print(message)
    

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Under Development",
            
        }),
    }
