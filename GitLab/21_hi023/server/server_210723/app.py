import socket
from flask import Flask
from flask import jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import sys
from datetime import datetime
import apscheduler.schedulers.blocking
import time
import cameraRP
from threading import Thread

app = Flask(__name__)

@app.route("/")
def print_hello():
    return 'test'


@app.route("/info", methods=["POST"])
def info():
    info_dict = dict()
    info_dict["IP_ADDRESS"] = socket.gethostbyname(socket.gethostname())
    info_dict["HOST_NAME"] = socket.gethostname()
    return info_dict

def loop():
    while True:
        print(111)
        time.sleep(3)

if __name__ == "__main__":
    sc = cameraRP.Socket()
    #sc.run_server()
    t=Thread(target=sc.run_server)
    t.start()
    t2 = Thread(target=loop)
    t2.start()
    app.run(debug=False, host="0.0.0.0", port=5000)
