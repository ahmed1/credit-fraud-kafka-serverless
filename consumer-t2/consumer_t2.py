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
    
    
    print('processed messages:', message)
    
    
    #put transaction in purchases database and update average in user db
    
    message['date'] = message['trans_date_trans_time'].split(" ")[0]
    
    #log transaction
    row = {}
    row['uuid'] = message['uuid']
    row['detais'] = [message['category'], Decimal(str(float(message['amt']))), message['city'], message['date']]
    # save_transaction = purchases.put_item(Item=app.to_decimal(message)) # edit this
    save_transaction = purchases.update_item(
        Key = {
            'uuid' : row['uuid']
        },
        UpdateExpression="SET details = list_append(details, :i)",
        ExpressionAttributeValues={
            ':i': [row],
        },
        ReturnValues="UPDATED_NEW"
    )
    

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
    # try:
    curr_user = client.get_item(TableName = 'credit-card-purchases', Key = {'uuid' : {'S' : str(message['uuid'])}  } )
    print('got here1', curr_user['Item'])
    curr_user = curr_user['Item']
    
    print('got here 2', message)
    print('count: ', curr_user['count'], 'AVG TRANS', curr_user['avgTransaction'])
    message['avgTransaction'] = (float(curr_user['count']['N'])-1) * float(curr_user['avgTransaction']['N']) / float(curr_user['count']['N'])
    
    message['count']  = int(curr_user['count']['N']) + 1
    print('got here 3', message)
    # except:
    #     print('went to except')
    #     pass
    
    # curr_user = user.get_item(Key={'uuid': message['uuid']})['Item']
    
    print("dumps", json.dumps(message['uuid']))
    #update average and count
    

    #update user table
    # client = boto3.client('dynamodb')
    
    row = {}
    
    row['uuid'] = message['uuid']
    row['avgTransaction'] = Decimal(str(float(message['avgTransaction'])))
    row['count'] = Decimal(str(float(message['count'])))
    
    
        
    user.put_item(Item=row)
    
    
    print('finished!')

        

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Messages Received",
            
        }),
    }
