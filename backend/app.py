import os
import json

from flask import Flask, request, jsonify

import sys
import traceback
from io import StringIO
import contextlib

app = Flask(__name__)

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def evaluate(code):
    with stdoutIO() as s:
        try:
            exec(code)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exc(limit=2, file=sys.stdout)
    return s.getvalue()

@app.route('/')
def get_name():
    target = os.environ.get('TARGET', 'Online')
    return '{}'.format(target)

@app.route('/eval', methods=['POST'])
def eval():
    payload = request.get_json(force=True)
    return_payload = {'result': evaluate(payload['script'])}
    return jsonify(return_payload)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8090)))
