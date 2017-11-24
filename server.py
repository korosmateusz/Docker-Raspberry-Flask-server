#!/usr/bin/python

from flask import Flask, request
from multiprocessing import Lock
from IPy import IP
import os
import time

mutex = Lock()
logdir = 'logs/'
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def getData():
    if request.method == 'GET':
        ip = request.args.get('ip', type = str)
        try:
            IP(ip)
        except:
            return 'Please specify proper IP'
        logfile = logdir + ip
        with mutex:
            if not os.path.isfile(logfile):
                return 'No data received yet'
            with open(logfile, 'r') as f:
                return f.read()
    elif request.headers['Content-Type'] == 'text/plain':
        logfile = logdir + request.remote_addr
        with mutex:
            with open(logfile, 'ab+') as f:
                f.write(time.strftime('%Y.%m.%d, %H:%M:%S >> ' ) + request.data + '\n')
            return 'Received data: ' + request.data

if __name__ == '__main__':
    with mutex:
        if not os.path.exists(logdir):
            os.makedirs(logdir)
    app.run(debug=True, host='0.0.0.0')
