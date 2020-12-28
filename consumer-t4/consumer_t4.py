import json
import boto3
import base64
# import requests
import csv
from datetime import date

today = date.today()
today = str(today.year) + str(today.month) + str(today.day - 1)
dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table = dynamodb.Table('test-purchases')
s3 = boto3.resource('s3')
bucket = s3.Bucket('cc-final-project-part3-backend')


def lambda_handler(event, context):
    event= event['records']['generate_reports-0']
    # print(len(event))
    event = [elem['value'] for elem in event]
    messages = [message.encode('utf-8') for message in event]
    messages = [base64.decodebytes(message).decode('utf-8') for message in messages] # json objects you can write to dynamodb
    
    
    
    # generate object for uuid (user)
    for message in messages:
        user = client.get_item(TableName = 'credit-card-purchases', Key = {'uuid' : {'S' : str(message)}  } )
        
    # write object to file in /tmp folder
        w = csv.writer(open("/tmp/{}.csv".format(message), "w"))
        for key, val in user.items():
            print(key, val)
            w.writerow([key, val])
    
    # copy object from /tmp to s3 using month/uuid
        key = '{}/{}.csv'.format(today, message)
        bucket.upload_file('/tmp/{}.csv'.format(message), key)
        
        
    
    
    
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
