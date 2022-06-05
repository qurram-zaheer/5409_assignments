from crypt import methods
from flask import Flask, request
import hashlib
import os
from pathlib import Path

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_checksum():
    try:
        file = request.json['file']
        md5 = hashlib.md5(
            open(os.path.join('', '/data', file), 'rb').read()).hexdigest()
        return {"file": file, "checksum": md5}, 200
    except FileNotFoundError:
        return {"file": file, "error": "File not found."}
