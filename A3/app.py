import base64

import rsa
from flask import Flask, request
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/decrypt', methods=['POST'])
def decrypt():
    b64_msg = request.json['message']
    decoded_msg = base64.b64decode(b64_msg)
    print(f'message: {decoded_msg}')
    with open("private_key.txt", 'r') as f:
        key = RSA.importKey(f.read())
    oaep_cipher = PKCS1_OAEP.new(key)
    hacked_msg = oaep_cipher.decrypt(decoded_msg)
    return {'response': hacked_msg.decode('utf-8')}


@app.route('/encrypt', methods=['POST'])
def encrypt():
    msg = request.json['message'].encode('utf-8')
    with open('public_key.txt', 'r') as f:
        key = RSA.importKey(f.read())
    oaep_cipher = PKCS1_OAEP.new(key)
    encrypted_msg = oaep_cipher.encrypt(msg)
    encrypted_msg = base64.b64encode(encrypted_msg)

    return {
               'response': encrypted_msg.decode('utf-8')
           }, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
