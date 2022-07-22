import json

import boto3


def lambda_handler(event, context):
    email = event['email']
    msg = event['message']
    
    if email == "rhawkey@dal.ca":
        return {
            'tier': 3,
            'result': {
                'email': event['email'],
                'message': event['message']
            }
        }
        
    if 'computer' in msg or 'laptop' in msg or 'printer' in msg:
        return {
            'tier': 2,
            'result': {
                'email': event['email'],
                'message': event['message']
            }
        }
        
    if 'account' in msg or 'password' in msg:
        return {
            'tier': 1,
            'result': {
                'email': event['email'],
                'message': event['message']
            }
        }
        
    return {
        'tier': 'unknown',
        'result': {
                'email': event['email'],
                'message': event['message']
            }
    }
