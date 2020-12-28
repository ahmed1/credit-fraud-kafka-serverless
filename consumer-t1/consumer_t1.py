import json
import base64
import boto3
from decimal import Decimal

# import requests

dynamo = boto3.resource('dynamodb')
user = dynamo.Table('credit-card-purchases')

client = boto3.client('lambda')

categories_vector = ['category_entertainment','category_food_dining','category_gas_transport','category_grocery_net','category_grocery_pos','category_health_fitness', 'category_home',	'category_kids_pets','category_misc_net','category_misc_pos','category_personal_care','category_shopping_net','category_shopping_pos','category_travel']
category_stats = {'min': {'entertainment': -0.4325895030466854,
  'food_dining': -0.4325895030466854,
  'gas_transport': -0.4018377451818567,
  'grocery_net': -0.42984492425144716,
  'grocery_pos': -0.3710236105262273,
  'health_fitness': -0.4325895030466854,
  'home': -0.4325895030466854,
  'kids_pets': -0.4325895030466854,
  'misc_net': -0.4325895030466854,
  'misc_pos': -0.4325895030466854,
  'personal_care': -0.4325895030466854,
  'shopping_net': -0.4325895030466854,
  'shopping_pos': -0.4325895030466854,
  'travel': -0.4325895030466854},
 'mean': {'entertainment': -0.03830317967052782,
  'food_dining': -0.1201634620554567,
  'gas_transport': -0.04314268059007756,
  'grocery_net': -0.10405041890986662,
  'grocery_pos': 0.29073791307518,
  'health_fitness': -0.10085637955875502,
  'home': -0.0753567577772238,
  'kids_pets': -0.07993064850790682,
  'misc_net': 0.0655833285479193,
  'misc_pos': -0.04653331532343699,
  'personal_care': -0.13962019985331636,
  'shopping_net': 0.11273382913548838,
  'shopping_pos': 0.058809586066795774,
  'travel': 0.2567034751401503},
 'max': {'entertainment': 5.390096787842075,
  'food_dining': 4.359569827020911,
  'gas_transport': 0.5219625265790198,
  'grocery_net': 0.7201959677441829,
  'grocery_pos': 2.0435819613754296,
  'health_fitness': 3.2936752258156536,
  'home': 3.059325622776787,
  'kids_pets': 3.218573569691407,
  'misc_net': 25.03797499183554,
  'misc_pos': 16.42548673237789,
  'personal_care': 2.84861682345145,
  'shopping_net': 59.163818224664816,
  'shopping_pos': 60.40798569397895,
  'travel': 180.1351207394022}}
  
state_stats = {'min': {'AK': -0.4325895030466854,
  'AL': -0.4325895030466854,
  'AR': -0.4325895030466854,
  'AZ': -0.4325271262558845,
  'CA': -0.4325895030466854,
  'CO': -0.4325271262558845,
  'CT': -0.4325271262558845,
  'DC': -0.4325895030466854,
  'DE': -0.37064934978142206,
  'FL': -0.4325895030466854,
  'GA': -0.4325895030466854,
  'HI': -0.4325895030466854,
  'IA': -0.4325895030466854,
  'ID': -0.4325895030466854,
  'IL': -0.4325895030466854,
  'IN': -0.4325895030466854,
  'KS': -0.4325895030466854,
  'KY': -0.4325895030466854,
  'LA': -0.4325895030466854,
  'MA': -0.4325895030466854,
  'MD': -0.4325895030466854,
  'ME': -0.4325271262558845,
  'MI': -0.4325895030466854,
  'MN': -0.4325895030466854,
  'MO': -0.4325895030466854,
  'MS': -0.4325895030466854,
  'MT': -0.4325895030466854,
  'NC': -0.4325895030466854,
  'ND': -0.4325895030466854,
  'NE': -0.4325895030466854,
  'NH': -0.4325895030466854,
  'NJ': -0.4325895030466854,
  'NM': -0.4325895030466854,
  'NV': -0.4325895030466854,
  'NY': -0.4325895030466854,
  'OH': -0.4325895030466854,
  'OK': -0.4325895030466854,
  'OR': -0.4325895030466854,
  'PA': -0.4325895030466854,
  'RI': -0.4323399958834819,
  'SC': -0.4325895030466854,
  'SD': -0.4325895030466854,
  'TN': -0.4325895030466854,
  'TX': -0.4325895030466854,
  'UT': -0.4325895030466854,
  'VA': -0.4325895030466854,
  'VT': -0.4325271262558845,
  'WA': -0.4325895030466854,
  'WI': -0.4325895030466854,
  'WV': -0.4325895030466854,
  'WY': -0.4325895030466854},
 'mean': {'AK': -0.013302571993107998,
  'AL': -0.030573057057570536,
  'AR': 0.030590648587615194,
  'AZ': 0.029332079561360625,
  'CA': 0.01915730604896143,
  'CO': 0.05109636067567558,
  'CT': -0.035245636404665555,
  'DC': 0.039599971930983066,
  'DE': 2.77041712005076,
  'FL': 0.022401118689154984,
  'GA': -0.0029918523058287605,
  'HI': -0.07079429309304852,
  'IA': -0.029664723941893623,
  'ID': 0.01693540376553904,
  'IL': -0.004460878753382141,
  'IN': -0.009994710963876876,
  'KS': -0.006479065365535849,
  'KY': -0.02550715554436307,
  'LA': 0.028739402458392155,
  'MA': -0.05396994813775028,
  'MD': -0.03406107885403901,
  'ME': -0.042436285725306735,
  'MI': 0.004830676534909169,
  'MN': -0.005768125947613346,
  'MO': -0.010433937404399147,
  'MS': -0.018834964389920092,
  'MT': -0.006518157455923148,
  'NC': 0.04133382830253186,
  'ND': -0.030263796478546892,
  'NE': -0.019382280456770158,
  'NH': 0.022821283974013902,
  'NJ': -0.02455805294558948,
  'NM': -0.05765421295685614,
  'NV': -0.08617077843175992,
  'NY': 0.009869400476951295,
  'OH': 0.016940308707761743,
  'OK': -0.02012170042677448,
  'OR': 0.0004215988235698209,
  'PA': 0.012006354715731398,
  'RI': 0.07228449908810396,
  'SC': -0.03764517001195577,
  'SD': 0.0017975990161820327,
  'TN': 0.027919655983540483,
  'TX': 0.008303188064609952,
  'UT': -0.03715733851250506,
  'VA': 0.0023338181188195775,
  'VT': 0.07325723927399319,
  'WA': 0.021371096430226347,
  'WI': -0.008916737452676881,
  'WV': 0.00295232453751945,
  'WY': 0.03372833135616043},
 'max': {'AK': 19.387698150720382,
  'AL': 65.21318177332392,
  'AR': 83.9996364963574,
  'AZ': 14.48974778345451,
  'CA': 70.81312054426279,
  'CO': 50.81761648513607,
  'CT': 51.1271924978808,
  'DC': 31.167243209510573,
  'DE': 5.878507059812883,
  'FL': 95.03477693373002,
  'GA': 74.16986516442077,
  'HI': 19.641509312489116,
  'IA': 48.294662427613304,
  'ID': 20.58545728767868,
  'IL': 35.315050290605186,
  'IN': 61.51267865906235,
  'KS': 21.40421504373089,
  'KY': 23.616283175902122,
  'LA': 46.2566879185673,
  'MA': 156.0454536392696,
  'MD': 47.64182693509141,
  'ME': 26.69838278616388,
  'MI': 90.8226593813197,
  'MN': 92.18908536060354,
  'MO': 59.163818224664816,
  'MS': 53.470626151478655,
  'MT': 22.53791321653669,
  'NC': 47.88902615703525,
  'ND': 28.69269354164928,
  'NE': 180.1351207394022,
  'NH': 73.61620876927225,
  'NJ': 48.623388115133885,
  'NM': 41.25818616453042,
  'NV': 18.710161449041337,
  'NY': 170.41195134294426,
  'OH': 61.934158634503824,
  'OK': 168.72559480364276,
  'OR': 31.92100434954828,
  'PA': 111.19841235716851,
  'RI': 72.10126365109154,
  'SC': 165.1348748411907,
  'SD': 43.18519236274169,
  'TN': 24.833878132335094,
  'TX': 93.4197170663139,
  'UT': 35.74900562420684,
  'VA': 74.57113505964277,
  'VT': 27.768643762725198,
  'WA': 43.053577334151846,
  'WI': 39.62591030285328,
  'WV': 70.49574743266797,
  'WY': 88.37393370484996}}
  
  
def lambda_handler(event, context):
    
    print('EVENTS:', event)
    
    messages = [event['records'][key][0]['value'] for key in event['records'].keys()]
    messages = [message.encode('utf-8') for message in messages]
    messages = [base64.decodebytes(message) for message in messages]
    
    
    print("len of og messages", len(messages))
    message_lst = []
    for message in messages:
        try:
            eval(message)['uuid']
            message_lst.append(eval(message))
        except:
            print("in except")
            pass

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
            amt = message['amt'] # normalize this
            state = message['state']
            category = message['category']

            state_min = state_stats['min'][state]
            state_mean = state_stats['mean'][state]
            state_max = state_stats['max'][state]
            category_min = category_stats['min'][category]
            category_mean = category_stats['mean'][category]
            category_max = category_stats['max'][category]
            
            penalty = 2.0
            
            cat_vec = [1 if category == c else 0 for c in categories_vector]
            
            left = [amt, state_min, state_mean, state_max, category_min, category_mean, category_max, penalty]
            
            payload = left + cat_vec
            payload = [str(x) for x in payload]
            payload = ','.join(payload)
            
            # deployed sagemaker instance with 
            # trained XGBoost Model
            sagemaker_endpoint = 'sagemaker-xgboost-2020-12-28-00-17-33-196' 
            response = runtime.invoke_endpoint(EndpointName = sagemaker_endpoint,
                                        ContentType = 'text/csv',
                                        Body = payload)
            response = response['Body'].read().decode('utf-8')
            
            res = False if response < 0.5 else True # 0 or 1
            
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
    
    