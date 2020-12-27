import json

# import requests


def lambda_handler(event, context):
    print('event:', event)
    
    messages = [event['records'][x][0]['value'] for x in event['records'].keys()]
    for message in messages:
        print(message)
    

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Under Development",
            
        }),
    }
