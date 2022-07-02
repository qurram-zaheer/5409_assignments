import logging
import boto3
from botocore.exceptions import ClientError
import os


def upload_file(file_name, bucket, object_name=None, region='us-east-1'):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name.split('/')[1])

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        print('Uploading file...')
        s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL': 'public-read'})
        print('Uploaded file!')
        return {'s3uri': f'https://{bucket}.s3.{region}.amazonaws.com/{object_name}'}
    except ClientError as e:
        print('ERROR: ', e)
        return None


def read_file(file_name, bucket, region='us-east-1'):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, file_name)
    data = obj.get()['Body'].read().decode('utf-8')
    return data


def delete_file(file_name, bucket):
    s3 = boto3.resource('s3')
    s3.Object(bucket, file_name).delete()
    return True
