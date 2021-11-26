from flask import Flask
import socketcom
from threading import Thread
from flask import request
import json

app = Flask(__name__)

@app.route("/")
def print_hello():
    return 'AI 살균'

@app.route("/sensor")
def get_sensor():
    '''
    list_name = sc.get_roomName()
    list_value = sc.get_sensor_value()
    list_sensor=[]
    for i, v in enumerate(list_name):
        sensor_dict = dict()
        sensor_dict['name']=v
        sensor_dict['temperature']=list_value[i][0]
        sensor_dict['humidity']=list_value[i][1]
        list_sensor.append(sensor_dict)
    '''
    data = json.dumps([{'name':'거실','temperature':20, 'humidity':30},{'name':'방1','temperature':30, 'humidity':40},
            {'name':'방2','temperature':35, 'humidity':50}])
    return data # list

@app.route("/clean")
def command_clean():
    id = request.args.get('id',"empty")
    if id=="empty":
        '''
        list_name = sc.get_roomName()
        list_id = sc.get_STEID()
        list_clean=[]
        for i, v in enumerate(list_id):
            clean_dict = dict()
            clean_dict['id'] = v
            clean_dict['name'] = list_name[i]
            list_clean.append(clean_dict)
        '''
        data = json.dumps([{'id':'STE-0-0000', 'name':'거실'},{'id':'STE-1-1111', 'name':'방1'},{'id':'STE-2-2222', 'name':'방2'}])
        return data
    #sc.command_clean_app(id=id)
    print(id)
    return "success"

@app.route("/document")
def get_document():
    data = sc.get_document()
    return data

@app.route("/effect")
def get_effect():
    data = sc.get_effect()
    return data

if __name__ == "__main__":
    sc = socketcom.Socket()

    # 소켓통신 및 메인 스레드 실행
    t1=Thread(target=sc.run_server)
    t1.start()

    # 살균명령 스레드 실행 - 미완
    t2=Thread(target=sc.command_clean)
    t2.start()

    app.run(debug=False, host="0.0.0.0", port=5000)