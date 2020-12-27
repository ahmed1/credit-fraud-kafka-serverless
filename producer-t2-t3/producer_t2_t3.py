import json
from kafka import KafkaProducer
import base64


def lambda_handler(event, context):
    producer = KafkaProducer(security_protocol="SSL", bootstrap_servers = ['b-2.kafkacluster4.quil2t.c11.kafka.us-east-1.amazonaws.com:9094',\
                                                                            'b-1.kafkacluster4.quil2t.c11.kafka.us-east-1.amazonaws.com:9094'])
                                                                            

    print(json.dumps(event))
    message = str(event)
    message_bytes = message.encode('utf-8')
    
    print(message_bytes)
    #check is_fraud
    
    if event['is_fraud']:
        topic = "not_approved"
        producer.send(topic, value=message_bytes)
        print("is Fraud")

    else:
        topic = "approved"
        producer.send(topic, value=message_bytes)
        print("is NOT Fraud")
        
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
