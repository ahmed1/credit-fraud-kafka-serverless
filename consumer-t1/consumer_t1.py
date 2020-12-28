import json
import base64
import boto3
from decimal import Decimal

# import requests

dynamo = boto3.resource('dynamodb')
user = dynamo.Table('credit-card-purchases')

client = boto3.client('lambda')

import sys
sys.path.append("/opt")
import app
  
  
def lambda_handler(event, context):
    
    print('EVENTS:', event)
    
    messages = [event['records'][key][0]['value'] for key in event['records'].keys()]
    messages = [message.encode('utf-8') for message in messages]
    message = [base64.decodebytes(message) for message in messages][0]
    
    
    print("len of og messages", len(messages))
    message_lst = []
    
    
    if 'uuid' in eval(message).keys():
        message_lst.append(eval(message))
    else:
        print("No uuid found!", eval(message))
        

    print("len of valid messages", len(message_lst))

    #based on extracted uuid, get user's transaction history
    for message in message_lst:
        #check if user is in database
        print(message)
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
            # check
            state_stats = app.state_stats
            amt = message['amt'] # normalize this
            state = message['state']
            category = message['category']
            category_stats = app.category_stats
            state_min = state_stats['min'][state]
            state_mean = state_stats['mean'][state]
            state_max = state_stats['max'][state]
            category_min = category_stats['min'][category]
            category_mean = category_stats['mean'][category]
            category_max = category_stats['max'][category]
            
            penalty = 2.0
            categories_vector = app.categories_vector
            cat_vec = [1 if category == c else 0 for c in categories_vector]
            
            left = [amt, state_min, state_mean, state_max, category_min, category_mean, category_max, penalty]
            
            payload = left + cat_vec
            payload = [str(x) for x in payload]
            payload = ','.join(payload)
            
            # deployed sagemaker instance with 
            # trained XGBoost Model
            sagemaker_endpoint = 'sagemaker-xgboost-2020-12-28-00-17-33-196'
            runtime = boto3.Session().client('sagemaker-runtime') 
            response = runtime.invoke_endpoint(EndpointName = sagemaker_endpoint,
                                        ContentType = 'text/csv',
                                        Body = payload)
            response = response['Body'].read().decode('utf-8')
            print('response:', response)
            
            res = False if float(response) < 0.5 else True # 0 or 1
            
            message['is_fraud'] = res
    
        print(json.dumps(message))
    
    
    #for each message trigger deny/approve lambda function
    for message in message_lst:
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
    
    