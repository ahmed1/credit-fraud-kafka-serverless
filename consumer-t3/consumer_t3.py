import json
import base64
import boto3
from decimal import Decimal

# import requests

dynamo = boto3.resource('dynamodb')
rejected = dynamo.Table('rejected-transactions')

def lambda_handler(event, context):
    messages = [event['records'][key][0]['value'] for key in event['records'].keys()]
    messages = [message.encode('utf-8') for message in messages]
    messages = [base64.decodebytes(message) for message in messages]
    messages = [eval(message) for message in messages] # json objects you can write to dynamodb
     
    
    for message in messages:
        message['date'] = message['trans_date_trans_time'].split(" ")[0]
        
        try:
            day = day.get_item(Key={'date': message['date']})
            day['Item']
        except:
            curr_user = None

        if curr_user == None:
            item = {
                'date': message['date'],
                'uuids': [message['uuid']]
            }
            day.put_item(Item=item)
        else:
            day['uuids'].append(message['uuid'])
            rejected.put_item(Item=day)

    
    print('processed messages:', messages)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
