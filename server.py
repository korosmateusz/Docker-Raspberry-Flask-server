#!/usr/bin/python

from flask import Flask, request
import os
from multiprocessing import Lock

mutex = Lock()
logdir = 'logs'
logfile = logdir + '/data.log'
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def getData():
    if request.method == 'GET':
        with mutex:
            if not os.path.isfile(logfile):
                return 'No data received yet'
            with open(logfile, 'r') as f:
                return f.read()
    elif request.headers['Content-Type'] == 'text/plain':
        with mutex:
            with open(logfile, 'ab+') as f:
                f.write(request.data + '\n')
            return 'Received data: ' + request.data

if __name__ == '__main__':
    with mutex:
        if not os.path.exists(logdir):
            os.makedirs(logdir)
    app.run(debug=True, host='0.0.0.0')
