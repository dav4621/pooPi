import requests
import json

# dict processed by lambda function
payload = {
        "Action": "Publish",
        "topic": "arn:aws:sns:us-east-1:118022561476:pooPi_notify",
        "message": "Clean the litter box! Your iPad internet will be disabled until it is cleaned."
        }

# api gateway invoke url
url = 'https://ogdb2lmlg3.execute-api.us-east-1.amazonaws.com/default/publishSNSMessage'

# sends post request to api gateway
req = requests.post( url, data = payload )

print( req.text )
