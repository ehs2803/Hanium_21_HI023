import socket
from flask import Flask
from flask import request
from flask import jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import apscheduler.schedulers.blocking
import time
import socketcom
from threading import Thread
from pynput import keyboard

app = Flask(__name__)

@app.route("/")
def print_hello():
    return 'test'

@app.route("/getSensor")
def get_sensor():
    list = sc.get_CAMlist()
    size = str(len(list))
    sc.get_sensor()
    return 1

@app.route("/clean")
def command_clean():
    id = request.args.get('id',"error")
    if id=="error":
        return "error"
    sc.command_clean(id)
    return "success clean : "+id

@app.route("/document")
def get_document():
    id = request.args.get('id', "error")
    if id=="error":
        return "error"
    sc.get_document()
    return "success"

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
    sc = socketcom.Socket()
    # 소켓통신 및 메인 스레드 실행
    t1=Thread(target=sc.run_server)
    t1.start()

    # 살균명령 스레드 실행 - 미완
    t2=Thread(target=sc.commandClean)
    t2.start()

    # 스레드 테스트 루프 실행
    t3 = Thread(target=loop)
    t3.start()

    app.run(debug=False, host="0.0.0.0", port=5000)