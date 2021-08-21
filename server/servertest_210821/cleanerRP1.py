import socket
import pymysql
import datetime
from pigpio_dht import DHT11
from pyfirmata import Arduino, util
import time
from threading import Thread
import threading

lock = threading.Lock()

class CleanerRP():
    def __init__(self):
        # 데이터베이스 연결
        self.db = pymysql.connect(host='54.180.136.222',
                                  user='root',
                                  password='haniumhi_023',
                                  db='testdb',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        self.sensor = DHT11(4)
        self.board = Arduino('/dev/ttyACM0')
        self.command_humidity=[]

        self.thread_flag = False

    def connectSocket(self):
        HOST = '127.0.0.1'  # '192.168.0.28' #'127.168.111.255'  #'192.168.123.7'
        PORT = 8888
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        name = "STE-9-2222"
        self.s.send(name.encode(encoding='utf_8', errors='strict'))

    def clean(self, cleantime):
        self.board.digital[4].write(0)
        time.sleep(cleantime)
        self.board.digital[4].write(1)

    def get_temp_humidity(self):
        result = self.sensor.read()
        temp_c = result['temp_c']
        humidity = result['humidity']
        return str(temp_c)+','+str(humidity)

    def get_humidity(self):
        result = self.sensor.read()
        humidity = result['humidity']
        return str(humidity)

    def save_humidityEffect(self):
        while True:
            if self.thread_flag==True:
                break
            now = datetime.datetime.now()  # 현재 날짜 얻어오기
            formatted_data = now.strftime('%Y-%m-%d %H:%M')  # 현재 시간 문자열 포맷팅
            for i, v in enumerate(self.command_humidity):
                if v['time']==formatted_data:
                    result = self.get_humidity()
                    # save
                    lock.acquire()
                    self.cursor.execute('insert into cleaneffect values(%s,%s,%s)',
                                        (v['cleanid'], v['before'], result))  # 데이터 삽입
                    self.db.commit()
                    lock.release()
                    # delete
                    del self.command_humidity[i]
                    break


    def run(self):
        self.board.digital[4].write(1)
        t = Thread(target=self.save_humidityEffect)
        t.start()
        while True:
            data = self.s.recv(1024)
            if data=="sensor":
                value = self.get_temp_humidity()
                self.s.send(value.encode(encoding='utf_8', errors='strict'))
            else:
                commad = data.split('-') # "clean-"+str(self.cleanstrength[i])+"-"+self.STElist[i][0]+"="+formatted_data
                strength = commad[1]
                cleanid = commad[2] # formatted_data = now.strftime('%Y-%m-%d %H:%M')  # 현재 시간 문자열 포맷팅
                cleandate = commad[2].split('=')[1]
                date_datetime = datetime.datetime.strptime(cleandate, '%Y-%m-%d %H:%M')
                date = date_datetime + datetime.timedelta(minutes=5)
                date_str = date.strftime('%Y-%m-%d %H:%M')
                before_humidity = self.get_humidity()
                if strength==0:
                    self.clean(30)
                elif strength==1:
                    self.clean(60)
                else:
                    self.clean(120)
                command_humidity_dict = dict()
                command_humidity_dict['cleanid'] = cleanid
                command_humidity_dict['before'] = before_humidity
                command_humidity_dict['time'] = date_str
                self.command_humidity.append(command_humidity_dict)

        self.s.close()
        self.thread_flag = True

cr = CleanerRP()
cr.connectSocket()
cr.run()