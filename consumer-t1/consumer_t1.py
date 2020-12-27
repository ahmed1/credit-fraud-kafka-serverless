import json
import base64
import boto3
from decimal import Decimal

# import requests

dynamo = boto3.resource('dynamodb')
user = dynamo.Table('credit-card-purchases')

client = boto3.client('lambda')


def lambda_handler(event, context):
    print('EVENTS:', event)
    messages = [event['records'][key][0]['value'] for key in event['records'].keys()]
    messages = [message.encode('utf-8') for message in messages]
    messages = [base64.decodebytes(message) for message in messages]
    messages = [eval(message)  for message in messages]
    print('processed messages:', messages)
    
    #based on extracted uuid, get user's transaction history
    for message in messages:
        #check if user is in database
        try:
            curr_user = user.get_item(Key={'uuid': message['uuid']})
            curr_user['Item']
        except:
            curr_user = None

        if curr_user == None:
            user.put_item(Item={'uuid': message['uuid'], 'avgTransaction': (Decimal(str(message['amt']))), 'count':1})
            curr_user = user.get_item(Key={'uuid': message['uuid']}) #probably a better way to do this
        
        #if transaction exceeds avg history by 25%
        threshold = float(Decimal(curr_user['Item']['avgTransaction'])) * 1.25
        curr_transaction = float(Decimal(message['amt']))

        #if curr > threshold return 1
        if curr_transaction > threshold:
            message['is_fraud'] = True
        else:
            message['is_fraud'] = False
    
        print(json.dumps(message))
    
    
    #for each message trigger deny/approve lambda function
    for message in messages:
        print(json.dumps(message))
        response = client.invoke(
            FunctionName = 'arn:aws:lambda:us-east-1:922059106485:function:Producer_t2_t3',
            InvocationType = 'RequestResponse',
            Payload = json.dumps(message)
        )
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Received Messages",
            
        }),
    }
    
    