import json
import base64
import boto3
from decimal import Decimal

# import requests

dynamo = boto3.resource('dynamodb')
purchases = dynamo.Table('test-purchases')
user = dynamo.Table('credit-card-purchases')

def to_decimal(message):
    message['amt'] = Decimal(str(float(message['amt'])))
    message['lat'] = Decimal(str(float(message['lat'])))
    message['long'] = Decimal(str(float(message['long'])))
    message['merch_lat'] = Decimal(str(float(message['merch_lat'])))
    message['merch_long'] = Decimal(str(float(message['merch_long'])))
    
    return message 


def lambda_handler(event, context):
    print('EVENTS:', event)
    messages = [event['records'][key][0]['value'] for key in event['records'].keys()]
    messages = [message.encode('utf-8') for message in messages]
    messages = [base64.decodebytes(message) for message in messages]
    messages = [eval(message) for message in messages] # json objects you can write to dynamodb
    
    
    print('processed messages:', messages)
    
    
    #put transaction in purchases database and update average in user db
    for message in messages:
        
        save_transaction = purchases.put_item(Item=to_decimal(message))
        
        curr_user = user.get_item(Key={'uuid': message['uuid']})
        
        #update average and count
        message['count']  = curr_user['Item']['count'] + 1
        message['avgTransaction'] = (curr_user['Item']['count'] * curr_user['Item']['avgTransaction']) / (message['count'])

        #update user table
        user.put_item(Key={'uuid': message['uuid'], 'avgTransaction': message['avgTransaction'], 'count': message['count']})
        
        

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Messages Received",
            
        }),
    }
