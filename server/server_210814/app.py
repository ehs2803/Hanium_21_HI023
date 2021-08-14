from flask import Flask
import socketcom
from threading import Thread
from flask import request

app = Flask(__name__)

@app.route("/")
def print_hello():
    return 'test'

@app.route("/getSensor")
def get_sensor():
    list_name = sc.get_roomName()
    list_value = sc.get_sensor_value()
    str_return=str(len(list_name))+":"
    for i in range(len(list_name)):
        str_return+=list_name[i]
        str_return+=":"
        str_return+=list_value[i][0]
        str_return+=":"
        str_return+=list_value[i][1]
        str_return+=":"
    return "3:aa:20:50:bb:25:40:cc:30:60:" #str_return #"3:aa:20:50:bb:25:40:cc:30:60:"

@app.route("/clean")
def command_clean():
    id = request.args.get('id',"empty")
    if id=="empty":
        list_name = sc.get_roomName()
        list_id = sc.get_STEID()
        str_return = str(len(list_name))+"/"
        for i in list_name:
            str_return+=i
            str_return+=":"
        str_return+="/"
        for i in list_id:
            str_return+=i
            str_return+=":"
        return "3/aa:bb:cc:/STE-0-0000:STE-1-1111:STE-2-2222:" #str_return #"3/aa:bb:cc:/STE-0-0000:STE-1-1111:STE-2-2222:"
    sc.command_clean(id=id)
    print(id)
    return "success"

@app.route("/document")
def get_document():
    data = sc.get_document()
    return data


if __name__ == "__main__":
    sc = socketcom.Socket()
    # 소켓통신 및 메인 스레드 실행
    t1=Thread(target=sc.run_server)
    t1.start()

    # 살균명령 스레드 실행 - 미완
    #t2=Thread(target=sc.commandClean)
    #t2.start()


    app.run(debug=False, host="0.0.0.0", port=5000)