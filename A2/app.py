import os
import json
import time
from multiprocessing import Process
import re

from flask import Flask, request
import requests
from dotenv import load_dotenv

import aws_handler

FIRST_FILE_NAME = os.path.join('tmp', 'first_req')
SECOND_FILE_NAME = os.path.join('tmp', 'second_req')


def greet_target(url, source_ip):
    req_json = {'banner': 'b00902314', 'ip': source_ip}
    print('Making request to target server, body: ', req_json)
    x = requests.post(url=f'{url}/start', json=req_json)
    print(x.text)


app = Flask(__name__)


@app.route('/storedata', methods=['POST'])
def get_data():
    data = request.json
    print("Data: ", data)

    with open(FIRST_FILE_NAME, 'w') as f:
        f.write(data['data'])

    s3_response = aws_handler.upload_file(file_name=FIRST_FILE_NAME, bucket=os.environ.get('BUCKET_NAME'))
    print(s3_response)

    return s3_response


@app.route('/appenddata', methods=['POST'])
def append_data():
    data = request.json['data']
    file_content = aws_handler.read_file(FIRST_FILE_NAME.split('/')[1], bucket=os.environ.get('BUCKET_NAME'))
    updated_content = [file_content, data]
    print(updated_content)
    with open(SECOND_FILE_NAME, mode='wt') as f:
        f.write(''.join(updated_content))

    upload_response = aws_handler.upload_file(file_name=SECOND_FILE_NAME, object_name=FIRST_FILE_NAME.split('/')[1],
                                              bucket=os.environ.get('BUCKET_NAME'))

    return {}, 200


@app.route('/deletefile', methods=['POST'])
def delete_file():
    s3_uri = request.json['s3uri']
    s3_object_name = s3_uri.split('/')[-1]
    processed_uri = s3_uri.replace('https://', '')
    bucket_name = processed_uri.split('/')[0].split('.')[0]
    print(bucket_name, s3_object_name)

    aws_handler.delete_file(file_name=s3_object_name, bucket=bucket_name)

    return {}, 200


def run():
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    load_dotenv()

    p1 = Process(target=run)
    p2 = Process(target=greet_target, args=(os.environ.get("TARGET_URL"), os.environ.get('SOURCE_IP')))

    p2.start()
    p1.start()

    p1.join()
    p2.join()

    print('Execution complete')
