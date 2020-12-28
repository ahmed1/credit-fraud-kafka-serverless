import json
import base64
import boto3
from decimal import Decimal

# import requests

dynamo = boto3.resource('dynamodb')
rejected = dynamo.Table('rejected-transaction')

def lambda_handler(event, context):
    messages = [event['records'][key][0]['value'] for key in event['records'].keys()]
    messages = [message.encode('utf-8') for message in messages]
    messages = [base64.decodebytes(message) for message in messages]
    messages = [eval(message) for message in messages]
    # message_lst = []
    # try:
    #     message_lst.append(eval(message))
    # except:
    #     pass
    #     #messages = [eval(message) for message in messages] # json objects you can write to dynamodb
 
 
    
    for message in messages:
        print("message", message)
        message['date'] = message['trans_date_trans_time'].split(" ")[0]
        

        try:
            day = rejected.get_item(Key={'date': message['date']})
            day = day['Item']
        except:
            print("user doesnt exist 1")
            day = None
        
        
        if day == None:
            print("user doesn't exist")
            item = {
                'date': message['date'],
                'uuids': [message['uuid']]
            }
            rejected.put_item(Item=item)
        else:
            day['date'] = message['date']
            day['uuids'].append(message['uuid'])
            rejected.put_item(Item=day)

    

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }
