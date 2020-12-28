import json
from kafka import KafkaProducer
#from kafka import KafkaClient
# import requests
import base64
import boto3

uuids = ['0157eb59-096c-450b-85b7-b7b44f80c5d4',
 '02960c25-6d07-4ca1-a0db-912b51bca10b',
 '0351f506-bd1c-45dc-9a52-a99c4eaa7c1f',
 '039ded7f-96ad-4e15-8035-5f8433891063',
 '03efe16f-cd80-4439-83c4-7925ab23ec3e',
 '0560ca12-add4-4435-b8de-a67ed89f4ff6',
 '06279f19-353c-4aca-8042-646b8f94db40',
 '08e1be46-aa1e-4d04-a214-96d85e81147c',
 '098a19ca-96bf-4b5d-8449-ff7b1e401290',
 '0c80e6f3-421d-473b-a97c-7b2437807e3c',
 '0fc9b7cf-57be-4512-823a-09aad935b4dd',
 '0ff6bdd4-c559-44bd-a442-c1b64014fdeb',
 '10502c64-05c5-4d51-ba77-5a4f3ce2f754',
 '11b28b85-0e77-4b1a-9baa-928234929fc6',
 '15d970e6-6935-42cc-abca-f7ac3b5b3fbf',
 '1919fd4b-2070-4770-b585-262217b31a02',
 '19963e7b-e27b-4dff-8095-e8bc75ba570a',
 '1af3a8f4-eabe-4522-a603-d6bdad5252d4',
 '1c71c072-2013-4e05-a9e7-f1d5be303b31',
 '201b8c30-00ac-4281-91f9-7aa4507c6258',
 '20cfe050-8c44-4f26-8941-33e2fad02286',
 '20d2cf78-cd95-4cdf-8a4b-46f747375bbf',
 '23fe9263-1a07-456c-922e-1b28aecf17af',
 '25e1ad2d-ed5c-41c1-8a21-6c92d80f88bb',
 '28c96d58-02ed-4f9b-902b-51384804b003',
 '290c7356-10a6-44ad-b376-2b5be1fcd4cf',
 '2986895d-8a5c-412c-bfd9-20ae26d82e3c',
 '2f697b65-025c-46b1-aa0d-f409f597a25c',
 '2fd6a5d5-a90a-4832-b6ea-7b2c400223b8',
 '306ce8d7-e2af-496d-92b4-7b15e5f2d1b2',
 '30fa3a04-fd76-4fe3-aeea-f5b1b93ea7bb',
 '318a55a7-6c1d-4148-a9a9-a1eb6fd6ab24',
 '342f5adc-7590-4ba2-9a10-d993c3468d58',
 '360edcb1-6085-4775-824a-8affd923367e',
 '370738a1-7f03-4052-9529-98f97d9e00bc',
 '373bd47a-e1ca-4d04-95d3-2b8cb0d00255',
 '37be99ad-fac2-46cf-8864-c44747bd6b13',
 '39604705-bffc-4926-8824-9d2f1bbc3b14',
 '3978a8b0-dfed-4fd4-a53a-9c63e5490409',
 '3bdff3d9-1b61-41a5-ac22-525ed612d6b5',
 '41bc5606-0b15-4302-b967-8353e551261f',
 '47139e03-4913-4e79-be04-f6fd8dbdc49f',
 '47f98ccf-5c78-4e9f-b9d8-65ef59532ad5',
 '49b0020e-7842-4ed9-aa60-073f3f4864a2',
 '4b82b34b-7bab-4a0f-b1a2-c2a8466caf4a',
 '4c03ad2f-a09a-4cbb-af13-5995f044e79f',
 '4c1ce249-0267-40ce-b03a-e57297b0f29f',
 '4c84ed8c-c99c-46a3-a108-a26133884ccf',
 '4e15ff5f-7069-4d20-a454-16753f6eb3e8',
 '501b924c-0460-467b-bcac-bba43cd13c70',
 '56493e86-d89e-4f6a-8986-a864b6ba01b2',
 '5893dcb4-352e-4e2c-8cd0-9025f80e3f89',
 '58c1155e-dfa0-4ebd-a6c9-e91f79d5ba02',
 '58e6365e-2547-48f2-a557-8f7ce2038d1e',
 '59a136fd-49c8-4f34-8ee7-4fde2aa00b20',
 '59a1bf59-2f68-4dba-aac1-bacc47e81d5c',
 '59abbd10-bf7b-4be1-990d-7ff5ba63c904',
 '5b122a8d-befc-4561-9708-8f9f33037663',
 '5b5c3311-4794-440b-a8bd-2110d5f6f164',
 '5b75a5d7-8941-49b4-b3da-f60f64a1d1a1',
 '5c935e11-5d5a-46d8-8a5f-641523f56930',
 '5e7805ed-8394-4d1e-a4db-8d2a30be90e9',
 '5f28f231-f9e2-41ef-b627-821be6d74261',
 '6216be94-9c49-4c49-a80c-9ec6d35de218',
 '623b6b59-95ae-4eaf-9239-16ae034148ad',
 '66ad7cd5-b1e5-4ada-842c-514ad7c7dc59',
 '67072911-2679-4bef-9810-74bc63e20997',
 '69e48b49-63a7-4ae2-b56c-574e473b6eca',
 '6bc93a71-db12-44fb-84fa-b17b2cb9b4d9',
 '6e97c6d2-4efe-4e71-a46f-d0020ef4d20c',
 '72164e7f-921c-4051-bdbe-0704c44bbe72',
 '7701a971-3c72-48fd-a9a2-575d4ef52636',
 '7b94ed32-c092-4a51-b28c-72300ad074df',
 '7eb58bd8-e990-46ad-820d-37fb438cf074',
 '81e82386-5bea-4a22-9e6c-645d1248847e',
 '858bcabd-f4aa-4cee-8d80-8598a673a3d1',
 '8c7a9754-dc59-46c1-82e7-b7a358a5a3b7',
 '90fba82d-ff73-44fa-a4d1-c2e3d671dd38',
 '91cd3b63-01b2-4204-8fce-079380cf051f',
 '928dbc52-0dd0-4f04-b8ed-195fa47e37c0',
 '93d8ffc7-3a43-4634-8cd4-dad709c46efe',
 '949f5581-63d1-4416-8237-2243e9d79bed',
 '967b58fa-4290-4b7b-918b-1c38b60f426d',
 '96c7ff81-336d-42ee-80ef-e822f65e80ce',
 '98954f95-c0ff-45de-ae77-3467bc5b9ac5',
 '9902f6ce-6d60-4b10-b8c8-45609afd9876',
 '9b733bd6-25fc-41e2-a1f0-a1d3fd627e66',
 '9bc86def-1e58-461c-a53d-61c2d3ee43e4',
 '9cbdf8e4-f7a9-419a-9ce5-a666c683b8d7',
 'a1df654d-8c14-4fa8-9fb1-e49c40377c89',
 'a20872a8-1bad-4d1c-acbd-3a174c699bc8',
 'a47ac1c6-d224-4f0d-9b54-4ea31ebc91b9',
 'a4b52f93-2dff-4308-bef8-377a1913c282',
 'a4ee5f97-97cf-4dee-83a9-89f4ef999dcd',
 'a5dcf507-7612-4b0e-b481-f28f27d122d8',
 'a7449dcb-175d-4174-8883-d749038ac88e',
 'aa61f9e5-2a48-4fe6-8a5b-446259b37ba7',
 'aa68bdec-2f1b-4043-a8a7-70e0979b6436',
 'abcfab30-49ff-4d6a-9766-4203965b82d8',
 'ad02b55e-fa7a-40eb-915f-4b6ed4fc5256',
 'b08bccc2-e4a1-4543-a96b-7cae6da35da9',
 'b20ba147-3726-40de-b3a4-2366ee4d7a43',
 'b3d84fe3-d554-47a8-b56a-7f915a510842',
 'b4221859-5597-443d-a8b1-75dc34434f7c',
 'b52dee3e-a6fa-477a-95bd-3554d52b200a',
 'b7f7aaaa-09d2-4304-9402-2a684800e974',
 'b8ce2067-f38b-4a4e-a64c-b87ad30b6c32',
 'b8d18e15-8437-45ef-8ad7-d0e65f8755f3',
 'bb8d7527-d4a8-464b-b9f8-acb77970f20d',
 'bbebd973-7f0c-438b-9b81-0491e7dcd3f5',
 'c29e6005-9d19-4c2f-a458-65c9a3d7b379',
 'c4e2ca77-d8bd-4ce2-96dd-b82aa38bad11',
 'c7360978-5879-4d88-bb60-aac7f4b47090',
 'c77333c2-d516-43fc-9be5-c63a01f7ce41',
 'c834bec3-31ce-4e52-8513-84653825b2a6',
 'cdeb4a8e-2cc8-449e-9583-f4f33f7fa323',
 'd019b118-1b00-4d79-bda4-db7599842bce',
 'd28cb5ce-a3be-468a-b3cd-b1b79c04a1d6',
 'd336d673-2d81-4893-bc93-3e88e9a4a38e',
 'd7c39fac-4ab1-42ba-89d8-f580047a6cff',
 'd84cd376-4767-45ce-b7b9-ba379c4260a8',
 'da068ae9-2be3-4086-9920-9bed379c0517',
 'db4fd1c2-059c-4f58-8209-bd963f10d173',
 'db9cb173-77fd-4c04-8d3a-c6edfc643906',
 'dc8da861-5280-4cf2-91f8-840ad41221cc',
 'de15ce11-7ab4-47ae-8568-e6fd6ae240ac',
 'e1379f7e-4b2e-443d-818d-f128f4ef8a7c',
 'e2b6c6c6-f45d-4a49-84da-3ff07707f8d0',
 'e373b3c2-a1a8-4ab8-afd3-48153ca43d91',
 'e4fcd95d-60af-4416-951e-02936754ca63',
 'e5d0c4ef-3d11-4064-bf88-997bcddf9fc0',
 'e68a1720-0af0-4895-bfa2-78380226b042',
 'e7d3856a-6c28-4396-96aa-95adba102409',
 'eb5e7be9-967c-4203-a0b1-c538409f5d0b',
 'ec43aa45-679d-4c1f-9906-ad02b38c694f',
 'ee17e407-89b8-4398-a45a-13bb047c605b',
 'f2496c90-5ba3-4f60-ae35-c942dfd230cb',
 'f3aec3a3-6c1e-4ed1-8340-9565b73ab0ae',
 'f3f4b4fd-3e1d-4be0-8e34-63d8e2b49d0d',
 'f59fa029-f754-40a1-8767-ff9a42cf6ade',
 'f5bca85e-2b3b-488a-beb5-c4d49cd83824',
 'f61564bb-5d14-4422-8a4c-73ade68234cc',
 'f92eceb4-c0c7-4f2d-9a91-1ee92944283c',
 'f96a50fe-c90e-4599-95c8-6b8c7d4a35a1',
 'f9f899c1-b0d5-46e0-a21f-877e9d1099bc',
 'fe2276df-d41e-412e-b8e5-49fca71d32ef',
 'febff031-48c7-416b-850c-67144e11d3f7',
 'ffa0b118-6d1e-4357-9347-519ab604b2bc',
 'ffd24d1c-a33a-40ba-a807-3ffdc226a470']


# generate_reports topic
def lambda_handler(event, context):
    
    

   
   
    producer = KafkaProducer(security_protocol="SSL", bootstrap_servers = ['b-2.kafkacluster4.quil2t.c11.kafka.us-east-1.amazonaws.com:9094',\
                                                                            'b-1.kafkacluster4.quil2t.c11.kafka.us-east-1.amazonaws.com:9094'])

    print(producer.bootstrap_connected())
    dynamo = boto3.resource('dynamodb')
    # fetch all unique uuids in dynamo
    table = dynamo.Table('test-purchases')
    
    for idx in range(0, len(uuids), 3):
        uuids_to_send = uuids[idx:idx + 2]
        uuids_to_send = ','.join(uuids_to_send)
        message_bytes = uuids_to_send.encode('utf-8')
        response = producer.send(topic='generate_reports', value = message_bytes)
        
        if idx % 10 == 0:
            print(idx, response)
        sys.sleep(2)
            
        
        
    
    # topic = str(event['resource'][1:]).replace('-', '_')
    # print(topic)
    # message = json.loads(event['body'])['body']
    # print('MESSAGE:', message)
    # message = str(message)
    # message_bytes = message.encode('utf-8')
    # #base64_bytes = base64.b64encode(message_bytes)
    
    
    # response = producer.send(topic=topic, value = message_bytes)
    
    # print('response', response)
    # if topic == 'authorize_purchase':
    #     msg = 'Received Validation Request'
    # else:
    #     msg = 'Received Purchase Record'
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Passed",
        }),
    }
