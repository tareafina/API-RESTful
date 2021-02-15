#import resources
import os
import json
import boto3
from todos import decimalencoder

#set dynamodb
dynamodb = boto3.resource('dynamodb')

#define function
def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch from database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    #translate
    translate = boto3.client('translate') 
    result_text = translate.translate_text(Text=result['Item']["text"],
                                  SourceLanguageCode="auto",
                                  TargetLanguageCode=event['pathParameters']['language'])
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result_text,
                           cls=decimalencoder.DecimalEncoder)
    }
    #return
    return response
