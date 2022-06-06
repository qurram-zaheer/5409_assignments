from flask import Flask, request
from werkzeug.exceptions import BadRequest
import hashlib
import os
import requests
from pathlib import Path

app = Flask(__name__)


@app.route("/checksum", methods=['POST'])
def get_checksum():
    try:
        body = request.json
        file = body['file']  # KeyError
        if file is None:
            return {"file": None, "error": "Invalid JSON input"}
        if file == "":
            return {"file": "", "error": "File not found."}
        print("File list", os.listdir(os.path.join('', '/data')))
        if not os.path.exists(os.path.join('', '/data', file)):
            return {"file": file, "error": "File not found."}
        if os.path.isdir(os.path.join('', '/data', file)):
            return {"file": file, "error": "File not found."}
        res = requests.post("http://container2:5000/", json={"file": file})
        print(res.json())
        return res.json(), 200
    except KeyError:
        return {"file": None, "error": "Invalid JSON input"}

    except BadRequest:
        return {"file": None, "error": "Invalid JSON input"}


@app.route("/", methods=["GET"])
def hello_world():

    return {"msg": "Hello world!"}, 200
