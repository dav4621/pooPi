import json
import requests
import time
import boto3


def sendRequestSNS():
    
    req = requests.get('https://ogdb2lmlg3.execute-api.us-east-1.amazonaws.com/default/publishSNSMessage')          # push get request to lambda trigger
    print( req.text )


def updateTable( level, statString ):

    t = time.localtime()                                # fetch time of code execution
    time_exec = time.strftime( "%I:%M %p", t )

    dynamodb = boto3.resource( 'dynamodb' )
    table = dynamodb.Table( 'sensorData' )
    table.update_item(                             # updates the table entry with specified values
        Key = {
            'id': '1'
        },
        UpdateExpression = 'SET sensor_level = :val1, statString = :val2, time_exec = :val3',
        ExpressionAttributeValues = {
            ':val1': level,
            ':val2': statString,
            ':val3': time_exec
        }
    )

    response = table.get_item(
        Key = {
            'id': '1'
        }
    )
    item = response[ 'Item' ]
    print( item )
