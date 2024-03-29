import json
from kafka import KafkaProducer
#from kafka import KafkaClient
# import requests
import base64


def lambda_handler(event, context):
    
    print('EVENT:', event) # for logging / debugging

   
   
    producer = KafkaProducer(security_protocol="SSL", bootstrap_servers = ['b-2.kafkacluster4.quil2t.c11.kafka.us-east-1.amazonaws.com:9094',\
                                                                            'b-1.kafkacluster4.quil2t.c11.kafka.us-east-1.amazonaws.com:9094'])

    print(producer.bootstrap_connected()) # make sure can establish connection with kafka
    
    topic = str(event['resource'][1:]).replace('-', '_')
    print(topic)
    message = json.loads(event['body'])['body']
    print('MESSAGE:', message)
    message = str(message)
    message_bytes = message.encode('utf-8')
    #base64_bytes = base64.b64encode(message_bytes)
    
    
    response = producer.send(topic=topic, value = message_bytes)
    
    print('response', response)
    if topic == 'authorize_purchase':
        msg = 'Received Validation Request'
    else:
        msg = 'Received Purchase Record'
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": msg,
        }),
    }
