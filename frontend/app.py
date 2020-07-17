import os
import requests

from flask import Flask, render_template, request

app = Flask(__name__)


ipExterna = 'http://35.202.177.228'
ipInterna = 'http://10.43.245.166'


def send_code(code):
    payload = {'script': code}
    response = requests.post(ipInterna + '/eval', json=payload)
    json_response = response.json()
    return json_response['result']

@app.route('/py', methods=['GET', 'POST'])
def py():
    code=''
    result=''
    if request.method == 'POST':
        code = request.form['code']
        result = send_code(code)
    return render_template('index.html', code=code, result=result)

@app.route('/')
def home():
    return render_template('index.html', code='', result='')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

