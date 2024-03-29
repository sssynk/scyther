from flask import Flask, request, jsonify
import requests
import json

app = Flask("Scyther")

registered_handlers = {} # dictionary of email to port
all_codes = {} # dictionary of email to code

@app.route('/')
def index():
    return 'scyther server is running'

@app.route('/send')
def send():
    global all_codes
    # data comes in as email,code
    email = request.args.get('email')
    code = request.args.get('code')
    all_codes[email] = code
    return 'failiure'

@app.route('/queue')
def queue():
    # return all_codes in json format
    return jsonify(all_codes)

print('scyther server is running')
app.run(host='0.0.0.0', port=8090)
