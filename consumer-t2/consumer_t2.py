import json
import base64
import boto3
from decimal import Decimal

# import requests
import sys
sys.path.append("/opt")

import app

dynamo = boto3.resource('dynamodb')
daily_purchases = dynamo.Table('daily_logs') #daily billing
purchases = dynamo.Table('test-purchases') #user billing
user = dynamo.Table('credit-card-purchases') #avgs




def lambda_handler(event, context):
    print('EVENTS:', event)
    messages = [event['records'][key][0]['value'] for key in event['records'].keys()]
    messages = [message.encode('utf-8') for message in messages]
    messages = [base64.decodebytes(message) for message in messages]
    message = [eval(message) for message in messages][0] # json objects you can write to dynamodb
    
    
    print('processed messages:', messages)
    
    
    #put transaction in purchases database and update average in user db
    
    message['date'] = message['trans_date_trans_time'].split(" ")[0]
    
    #log transaction
    save_transaction = purchases.put_item(Item=app.to_decimal(message))

    #check if day exists in date daily_purchases
    try:
        day = daily_purchases.get_item(Key={'date': message['date']})
        day = day['Item']
    except:
        day = None
    
    #if day does not exist create new object with details in list
    if day == None:
        item = {
            'date': message['date'],
            'details': [str(message)]
        }
        daily_purchases.put_item(Item=(item))
    
    #append details to existing object day
    else:
        # day['date'] = message['date']
        day['details'].append(str(message))
        daily_purchases.put_item(Item=(day))
        
    
    #user history of past purchases
    client = boto3.client('dynamodb')
    try:
        curr_user = client.get_item(TableName = 'credit-card-purchases', Key = {'uuid' : {'S' : str(message['uuid'])}  } )
        print(curr_user['Item'])
        curr_user = curr_user['Item']
        message['count']  = curr_user['Item']['count'] + 1
        message['avgTransaction'] = (curr_user['Item']['count'] * curr_user['Item']['avgTransaction']) / (message['count'])
    except:
        pass
    
    # curr_user = user.get_item(Key={'uuid': message['uuid']})['Item']
    
    print("dumps", json.dumps(message['uuid']))
    #update average and count
    

    #update user table
    # client = boto3.client('dynamodb')
    user.put_item(Key={'uuid': message['uuid'], 'avgTransaction': message['avgTransaction'], 'count': message['count']})
        
        

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Messages Received",
            
        }),
    }
