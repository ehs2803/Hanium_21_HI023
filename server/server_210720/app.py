import socket
from flask import Flask
from flask import jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import time
import cameraRP

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

if __name__ == "__main__":
    sc = cameraRP.Socket(8888);
    sc.startSC()
    sc1 = cameraRP.Socket(8889)
    while True:
        print(111)
        time.sleep(3)
    app.run(debug=False, host="0.0.0.0", port=5000)
